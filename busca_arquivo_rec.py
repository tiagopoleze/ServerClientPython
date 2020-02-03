import os
from datetime import datetime

# Buscar informações sobre arquivos e diretorios.
def busca_arquivo_rec(nome, dir):

    lista_dir =[]
    lista_resp = []
    lista_dir.append(dir)

    while lista_dir:
        dir_atual = lista_dir[0]
        l =[]
        try:
            l = os.listdir(dir_atual)
        except Exception as e:
            print(e)

        for i in l:
            arq = os.path.join(dir_atual, i)
            if os.path.isfile(arq) and i == nome:
                try:
                    nome_arquivo = i
                    tamanho_arquivo = os.path.getsize(i)
                    data_modificacao = datetime.fromtimestamp(os.path.getctime(i)).strftime('%Y-%m-%d %H:%M:%S')
                    lista_resp.append({
                        "nome": nome_arquivo,
                        "bytes": tamanho_arquivo,
                        "Data Modificacao": data_modificacao
                    })
                except:
                    pass
            elif os.path.isdir(arq):
                lista_dir.append(arq)

        lista_dir.remove(dir_atual)

    return (lista_resp)
