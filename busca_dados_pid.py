# Tiago Poleze Ferreira

import psutil

lista_processos = psutil.pids()
lista_enviar = []

def busca_dados_pid():

    for i in lista_processos:
        if psutil.pid_exists(i):
            processo = psutil.Process(i)
            try:
                nome_processo = processo.name()
                if nome_processo == 'Safari':
                    cpu_processo = str(processo.cpu_percent(interval=1))
                    memoria_processo = str(processo.memory_percent())
                    lista_enviar.append({
                        'nome_processo': nome_processo,
                        'cpu_processo': cpu_processo,
                        'memoria_processo': memoria_processo
                    })
            except Exception as e:

                pass

    return lista_enviar[0]


