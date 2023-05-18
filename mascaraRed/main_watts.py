from document import list_file
from device import Device_ssh
import subprocess
import threading
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
import pprint
from collections import Counter


'''
Con este script se obtiene el consumo de las interfaces.
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
        output_lines=device.ssh("cisco_ios",'show power inline')
        watts = device.watts(output_lines)
        print(ip,watts)
        return watts
    else:
        return 0


   

if __name__ == '__main__':

    ips = list_file("ips.txt")
    threads = list()
    results = []
    reference_device_total = {}
    reference_device_total_dict = []
    consumo_device_total_dict = []
    consumo_device_total = {}

    with ThreadPoolExecutor(max_workers=10) as executor:
        future_results = {executor.submit(main, ip): ip for ip in ips}
        for future in concurrent.futures.as_completed(future_results):
            ip = future_results[future]
            try:
                result = future.result()
            except Exception as exc:
                result = str(exc)

            try:
                results.append(float(result[0]))

                reference_device_total_dict.append(result[1])
                reference_device_total = sum((Counter(dic) for dic in reference_device_total_dict), Counter())

                consumo_device_total_dict.append(result[2])
                consumo_device_total = sum((Counter(dic) for dic in consumo_device_total_dict), Counter())
            except:
                pass

            
            
            
           
        
    total_watts = round(sum(results),2)
    total_kwatts = round(total_watts/1000,2)
    precio_kwh = 800
    total_kwatts_hora_24 = round(total_kwatts*24,2)
    total_kwatts_hora_15 = round(total_kwatts*15,2)
    total_kwatts_precio_24 = round(total_kwatts_hora_24*precio_kwh)
    total_kwatts_precio_15 = round(total_kwatts_hora_15*precio_kwh)

    total_kwatts_precio_24_mes = round(total_kwatts_precio_24*30)
    total_kwatts_precio_15_mes = round(total_kwatts_precio_15*30)
    dif1=total_kwatts_precio_24_mes-total_kwatts_precio_15_mes

    total_kwatts_precio_24_año = round(total_kwatts_precio_24*365)
    total_kwatts_precio_15_año = round(total_kwatts_precio_15*365)
    dif2=total_kwatts_precio_24_año-total_kwatts_precio_15_año

    
    print("#"*30,end="\n")
    print(""*2,end="\n")
    print(f"Total W {total_watts}W",end="\n")
    print(f"Total Kw {total_kwatts} Kw",end="\n")
    print(f"Precio kwh ${precio_kwh}",end="\n")
    print("",end="\n")
    print(f"Total kwh 24 {total_kwatts_hora_24} kwh",end="\n")
    print(f"Total kwh 15 {total_kwatts_hora_15} kwh",end="\n")
    print("",end="\n")
    print(f"Precio kwh 24 ${total_kwatts_precio_24} ",end="\n")
    print(f"Precio kwh 15 ${total_kwatts_precio_15} ",end="\n")
    print("",end="\n")
    print(f"Precio kwh 24 mes ${total_kwatts_precio_24_mes} ",end="\n")
    print(f"Precio kwh 15 mes ${total_kwatts_precio_15_mes} ",end="\n")
    print(f"Ahorro mes ${dif1} ",end="\n")
    print("",end="\n")
    print(f"Precio kwh 24 year ${total_kwatts_precio_24_año} ",end="\n")
    print(f"Precio kwh 15 year ${total_kwatts_precio_15_año} ",end="\n")
    print(f"Ahorro year ${dif2} ",end="\n")

    print("",end="\n")
    print(f"Los equipos encontrados son",end="\n")
    pprint.pprint(reference_device_total, width=1)
    print("",end="\n")
    print(f"Consumo por equipo",end="\n")
    pprint.pprint(consumo_device_total, width=1)
    print("",end="\n")
    

    


