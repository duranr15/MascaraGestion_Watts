import icmplib
import paramiko
from icmplib import multiping
import re
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
    ConnectionException,
    NetmikoBaseException,
    SSHDetect
    
)

'''
Se crea una clase para dispositivos ssh conectados al directorio activo, se tiene metodo para el envio de comandos por 
ssh, busqueda de la mascara de gestion y consumo de las interfaces.
'''


class Device_ssh():

    def __init__ (self,deviceType,ipAddress,username,password):
        self.deviceType = deviceType
        self.ipAddress = ipAddress
        self.username = username
        self.password = password
        self.readTimeoutOverride = 90

    def ping(self,):
        # Ping al dispositivo
        ping_obj = icmplib.ping(self.ipAddress, count=4, interval=0.2)
        if ping_obj.is_alive:
            return 1
        else:
            return 0

    
    def device(self,):
        # valores necesarios
        defineDevice= {
            "device_type": self.deviceType,
            "host": self.ipAddress,
            "username": self.username,
            "password": self.password,
            "read_timeout_override": 90,            
            }
        return defineDevice

    def autodetect(self,device):
        # Detecta que tipo de dispositivo es
        try:
            guesser = SSHDetect(**device)
            device_type = guesser.autodetect()
            return device_type
        except (NetmikoAuthenticationException,):
            return "0000"
        
    def ssh(self,device_type,comando):
        # conexion por ssh
        try:
            device= {
                "device_type": device_type,
                "host": self.ipAddress,
                "username": self.username,
                "password": self.password,
                "read_timeout_override": 90,            
                }

            with ConnectHandler(**device,fast_cli=False) as ssh:

                ssh.enable()
                output = ssh.send_command(comando,read_timeout=90,expect_string=r"#",delay_factor=30)                
                output_lines = [line.strip() for line in output.split("\n")]  
                ssh.disconnect()

            return output_lines
        except:
            return 0
        
    
    def ipGestion(self,output_lines):
        # obtiene la mascara de gestion
        ip_mask = "No encontrado"
        if output_lines != 0:
            for line in output_lines:  
                if self.ipAddress in line:
                    ip_mask = line
                    break
        return ip_mask
    
    def watts(self,output_lines):
        # consumo de las interfaz
        watts = 0
        referencia_dict = {}
        consumo_referencia_dict = {}
        
        if output_lines != 0:
            for line in output_lines:  
                if "on" in line:
                    watt = float(re.search(r'on\s+(\S+)', line).group(1))
                    watts += watt

                    # Se obtienen las referencias.
                    columna=line.split()
                    referencia_device = columna[4]


                    if ( referencia_device in referencia_dict ) and referencia_device != "0.0" :
                        referencia_dict[referencia_device] +=1
                        consumo_referencia_dict[referencia_device]  += watt
                    else:
                        referencia_dict[referencia_device] = 1
                        consumo_referencia_dict[referencia_device]  = watt
                    
        return watts, referencia_dict,consumo_referencia_dict

        

if __name__ == '__main__':

    D1 = Device_ssh("autodetect","10.10.10.10","user","password")
    s0=print(D1.ping())
    
    s1=D1.device()
    s3=D1.ssh("cisco_ios","show run")
    s4 = print(D1.ipGestion(s3))
    s5=D1.autodetect(s1)


    
    
    