import psutil

# Buscar informações sobre rede
def mostrar_dados_rede():
    info_rede = psutil.net_if_addrs()
    ip_dado = info_rede['lo0'][0].address
    mascara_dado = info_rede['lo0'][0].netmask
    protocolo_dado = str(info_rede['lo0'][0].family)
    if protocolo_dado == "AddressFamily.AF_INET":
        protocolo_dado = 'IPv4'
    if protocolo_dado == "AddressFamily.AF_INET6":
        protocolo_dado = 'IPv6'
    if protocolo_dado == "AddressFamily.AF_LINK":
        protocolo_dado = 'Enlace'

    return {
        'tipo': protocolo_dado,
        'ip': ip_dado,
        'mascara': mascara_dado
    }