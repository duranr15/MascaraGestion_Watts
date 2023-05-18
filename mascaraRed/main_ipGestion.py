from document import list_file
from device import Device_ssh
import subprocess
import threading

'''
Con este script se obtiene la mascara de la ip de gestion de manera asincrona.
Para entender este script sugiero estudiar la libreria de Netmiko, Paramiko y threading de python,
mas especificamente la conexión por ssh con dispositivos cisco.

No olvidar iniciar el venv (virtual environment) se hace de la siguiente manera en la ubicación del archivo.
source .venv/script/activate

En el archivo ips.txt poner por fila cada una de las ips de los dispositivos.
    10.10.10.10
    10.10.10.10
    10.10.10.10

En la función main, cambiar "user" y "password" por las credenciales
'''

def main(ip):
    
    device = Device_ssh("autodetect",ip,"user","password")
    device_ping = device.ping()
    if device_ping == 1:
        output_lines=device.ssh("cisco_ios",'show ip interface')
        print(ip,device.ipGestion(output_lines),end="\n")
    else:
        print(ip," sin ping " ,end="\n")


   

if __name__ == '__main__':

    ips = list_file("ips.txt")
    threads = list()

    for ip in ips:                    
        th = threading.Thread(target=main,args=(ip,))
        threads.append(th)
        th.start()

    for index, thread in enumerate(threads):
        thread.join()



