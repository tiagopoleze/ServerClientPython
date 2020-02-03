import socket, psutil, cpuinfo, os, pickle
import mostrar_dado_rede, busca_arquivo_rec, busca_dados_pid

dic = {}

socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = '0.0.0.0'
porta = 25000

socket_servidor.bind((host, porta))
socket_servidor.listen()

print("Servidor de nome " + host + " na porta " + str(porta))
(socket_cliente, addr) = socket_servidor.accept()
print("Conectado a:", str(addr))

while True:
    # Dados para serem enviados
    info_cpu = cpuinfo.get_cpu_info()
    nome_cpu = info_cpu["brand"]
    arquitetura_cpu = info_cpu["arch"]
    bits_cpu = info_cpu["bits"]
    freq = str(round(psutil.cpu_freq().current, 2))
    nucleos = str(psutil.cpu_count())
    nucleos = nucleos + " (" + str(psutil.cpu_count(logical=False)) + ")"
    dados_rede = mostrar_dado_rede.mostrar_dados_rede()
    dir = os.environ['PWD']
    dados_pasta = busca_arquivo_rec.busca_arquivo_rec('server.py', dir)
    dados_processo = busca_dados_pid.busca_dados_pid()
    processador = psutil.cpu_percent(interval=1, percpu=True)
    mem = psutil.virtual_memory()
    disco = psutil.disk_usage('.')

    dic = {
        "S1": [
            nome_cpu,
            arquitetura_cpu,
            bits_cpu,
            freq,
            nucleos,
            dados_rede,
            dados_pasta,
            dados_processo
        ],
        "S2": [processador],
        "S3": [mem],
        "S4": [disco]
    }

    msg = socket_cliente.recv(50)
    nome = msg.decode('utf-8')
    if nome == 'iniciando':
        dic_pickle = pickle.dumps(dic)
        socket_cliente.send(dic_pickle)
        print('informações enviadas com sucesso')
    else:
        socket_cliente.send('erro'.decode('utf-8'), 50)
        print('erro')


socket_cliente.close()
socket_servidor.close()