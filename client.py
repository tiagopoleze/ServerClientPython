import pygame, socket, pickle

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:

    s.connect(('0.0.0.0', 25000))

except Exception as e:
    print(e)


# Cores:
preto = (0, 0, 0)
branco = (255, 255, 255)
cinza = (100, 100, 100)
vermelho = (255, 0, 0)
azul = (0, 0, 255)

# Iniciando a janela principal
largura_tela = 1024
altura_tela = 768
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Informações de CPU")
pygame.display.init()

# Superfície para mostrar as informações:
s1 = pygame.surface.Surface((largura_tela, altura_tela/4))
s2 = pygame.surface.Surface((largura_tela, (altura_tela/4)))
s3 = pygame.surface.Surface((largura_tela, (altura_tela/4)))
s4 = pygame.surface.Surface((largura_tela, (altura_tela/4)))

# Para usar na fonte
pygame.font.init()
font = pygame.font.Font(None, 24)

# Cria relógio
clock = pygame.time.Clock()

# Contador de tempo
cont = 60

# Mostra texto de acordo com uma chave:
def mostra_texto(s1, nome, chave, pos_y):
  text = font.render(nome, True, preto)
  s1.blit(text, (10, pos_y))
  if chave == "freq":
      s = str(lista_pickle['S1'][3])
  elif chave == "nucleos":
      s = str(lista_pickle['S1'][4])
  elif chave == "ip":
      s = str(lista_pickle['S1'][5])
  elif chave == 'brand':
      s = str(lista_pickle['S1'][0])
  elif chave == 'arch':
      s = str(lista_pickle['S1'][1])
  elif chave == 'pid':
      s = str(lista_pickle['S1'][7])
  elif chave == 'pasta':
      s = str(lista_pickle['S1'][6][0])
  else:
      s = str(lista_pickle['S1'][2])
  text = font.render(s, True, cinza)
  s1.blit(text, (160, pos_y))


# Mostra as informações de CPU escolhidas:
def mostra_info_cpu(superficie):
    superficie.fill(branco)
    mostra_texto(superficie, "Nome:", "brand", 10)
    mostra_texto(superficie, "Arquitetura:", "arch", 30)
    mostra_texto(superficie, "Palavra (bits):", "bits", 50)
    mostra_texto(superficie, "Frequência (MHz):", "freq", 70)
    mostra_texto(superficie, "Núcleos (físicos):", "nucleos", 90)
    mostra_texto(superficie, "Dados da rede:", "ip", 110)
    mostra_texto(superficie, "Dados da pasta:", "pasta", 130)
    mostra_texto(superficie, "Processo:", "pid", 150)
    tela.blit(superficie, (0, 0))

# Mostrar uso de CPU:
def mostra_uso_cpu(superficie):
    superficie.fill(preto)
    num_cpu = len(lista_pickle['S2'][0])
    x = 10
    y = 20
    desl = 10
    alt = superficie.get_height() - 2*y
    larg = (superficie.get_width()-2*y - (num_cpu+1)*desl)/num_cpu
    d = x + desl
    for i in lista_pickle['S2'][0]:
          pygame.draw.rect(superficie, vermelho, (d, y, larg, alt))
          pygame.draw.rect(superficie, azul, (d, y, larg, (1-i/100)*alt))
          d = d + larg + desl
    # parte mais abaixo da tela e à esquerda
    tela.blit(superficie, (0, (altura_tela/4) + 20))
    text = font.render("Uso de CPU:", 1, branco)
    tela.blit(text, (20, (altura_tela/4)+10))


# Mostar uso de memória
def mostra_uso_memoria(superficie):
    alt = superficie.get_height()
    larg = superficie.get_width()
    pygame.draw.rect(superficie, azul, (10, 30, larg-40, alt-20))
    larg = larg*lista_pickle['S3'][0].percent/100
    pygame.draw.rect(superficie, vermelho, (10, 30, larg-40, alt-20))
    total = round(lista_pickle['S3'][0].total/(1024*1024*1024),2)
    texto_barra = "Uso de Memória (Total: " + str(total) + "GB):"
    text = font.render(texto_barra, 1, branco)
    tela.blit(superficie, (0, altura_tela/4*2))
    tela.blit(text, (10, (altura_tela/4*2) + 10))


# Mostrar o uso de disco local
def mostra_uso_disco(superficie):
    alt = superficie.get_height()
    larg = superficie.get_width()
    pygame.draw.rect(superficie, azul, (10, 30, larg-40, alt-20))
    larg = larg*lista_pickle['S4'][0].percent/100
    pygame.draw.rect(superficie, vermelho, (10, 30, larg-40, alt-20))
    total = round(lista_pickle['S4'][0].total/(1024*1024*1024), 2)
    texto_barra = "Uso de Disco: (Total: " + str(total) + "GB):"
    text = font.render(texto_barra, 1, branco)
    tela.blit(superficie, (0, altura_tela/4*3))
    tela.blit(text, (15, (altura_tela/4*3)+10))


terminou = False
# Repetição para capturar eventos e atualizar tela
while not terminou:
    # Checar os eventos do mouse aqui:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminou = True

    # Fazer a atualização a cada segundo:
    if cont == 60:
        s.send('iniciando'.encode('utf-8'), 50)
        lista = s.recv(4096)
        lista_pickle = pickle.loads(lista)
        mostra_info_cpu(s1)
        mostra_uso_cpu(s2)
        mostra_uso_memoria(s3)
        mostra_uso_disco(s4)
        cont = 0

    # Atualiza o desenho na tela
    pygame.display.update()

    # 60 frames por segundo
    clock.tick(60)
    cont = cont + 1

# Finaliza a janela
pygame.display.quit()
s.close()