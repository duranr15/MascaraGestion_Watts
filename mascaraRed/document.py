# Lee un txt y lo organiza en una lista.
def list_file(file):

    try:

        ips=[]

        with open(file, 'r') as f: 
            for line in f:
                ips.append(line.strip())

        return ips
    except:
        return "documento no encontrado"

