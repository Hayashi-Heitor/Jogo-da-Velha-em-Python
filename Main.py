import pygame, sys
import numpy as np

pygame.init()

#constantes
LARGURA = 600
ALTURA = LARGURA
LARGURA_LINHA = 15
FUNDO_LINHAS = 3
FUNDO_COLUNAS = 3
ESPAÇO = 55

RAIO_CIRCULO = 60
LARGURA_CIRCULO = 15
COR_FUNDO = (28, 170, 156)
COR_LINHA = (50, 145, 145)
COR_CIRCULO = (239, 231, 200)
COR_X = (66, 66, 66)

LARGURA_X = 25

tela = pygame.display.set_mode( (LARGURA, ALTURA) )
pygame.display.set_caption("Jogo da Velha")
tela.fill(COR_FUNDO)

#fundo
fundo = np.zeros( (FUNDO_LINHAS, FUNDO_COLUNAS) )
print(fundo)

#linhas
def linhas():
    pygame.draw.line(tela, COR_LINHA, (0,200), (600, 200), LARGURA_LINHA) #horizontal 1
    pygame.draw.line(tela, COR_LINHA, (0, 400), (600, 400), LARGURA_LINHA) #horizontal 2
    pygame.draw.line(tela, COR_LINHA, (200, 0), (200, 600), LARGURA_LINHA) #vertical 1
    pygame.draw.line(tela, COR_LINHA, (400, 0), (400, 600), LARGURA_LINHA) #vertical 2

def desenha_figuras():
    for linha in range(FUNDO_LINHAS):
        for coluna in range(FUNDO_COLUNAS):
            if fundo[linha][coluna] == 1:
                pygame.draw.circle(tela, COR_CIRCULO, (int(coluna * 200 + 200 / 2), int(linha * 200 + 100)), RAIO_CIRCULO, LARGURA_CIRCULO)
            elif fundo[linha][coluna] == 2:
                pygame.draw.line(tela, COR_X, (coluna * 200 + ESPAÇO, linha * 200 + 200 - ESPAÇO), (coluna*200 + 200 - ESPAÇO, linha * 200 + ESPAÇO), LARGURA_X)
                pygame.draw.line(tela, COR_X, (coluna * 200 + ESPAÇO, linha * 200 + ESPAÇO), (coluna * 200 + 200 - ESPAÇO, linha * 200 + 200 - ESPAÇO), LARGURA_X)


def quadrado_marcado(linha, coluna, jogador):
    fundo[linha][coluna] = jogador

def quadrados_disponiveis(linha, coluna):
    return fundo[linha][coluna] == 0

def velha():
    for linha in range(FUNDO_LINHAS):
        for coluna in range(FUNDO_COLUNAS):
            if fundo[linha][coluna] == 0:
                return False
    return True

def ganhar(jogador):

    #vertical
    for coluna in range(FUNDO_COLUNAS):
        if fundo[0][coluna] == jogador and fundo[1][coluna] == jogador and fundo[2][coluna] == jogador:
            linha_vertical_ganhar(coluna, jogador)
            return True

    #horizontal
    for linha in range(FUNDO_LINHAS):
        if fundo[linha][0] == jogador and fundo[linha][1] == jogador and fundo[linha][2] == jogador:
            linha_horizontal_ganhar(linha, jogador)
            return True

    #diagonal ascendente
    if fundo[2][0] == jogador and fundo[1][1] == jogador and fundo[0][2] == jogador:
        linha_diagonal_ascendente_ganhar(jogador)
        return True

    #diagonal descendente
    if fundo[0][0] == jogador and fundo[1][1] == jogador and fundo[2][2] == jogador:
        linha_diagonal_descendente_ganhar(jogador)
        return True

    return False

def linha_vertical_ganhar(coluna, jogador):
    posX = coluna * 200 + 100

    if jogador == 1:
        cor = COR_CIRCULO
    elif jogador == 2:
        cor = COR_X

    pygame.draw.line(tela, cor, (posX, 15), (posX, ALTURA-15), 15)

def linha_horizontal_ganhar(linha, jogador):
    posY = linha * 200 + 100

    if jogador == 1:
        cor = COR_CIRCULO
    elif jogador == 2:
        cor = COR_X

    pygame.draw.line(tela, cor, (15, posY), (LARGURA - 15, posY), 15)

def linha_diagonal_ascendente_ganhar(jogador):
    if jogador == 1:
        cor = COR_CIRCULO
    elif jogador == 2:
        cor = COR_X

    pygame.draw.line(tela, cor, (15, ALTURA - 15), (LARGURA - 15, 15), 15)

def linha_diagonal_descendente_ganhar(jogador):
    if jogador == 1:
        cor = COR_CIRCULO
    elif jogador == 2:
        cor = COR_X

    pygame.draw.line(tela, cor, (15, 15), (LARGURA - 15, ALTURA - 15), 15)

def restart():
    tela.fill(COR_FUNDO)
    linhas()
    jogador = 1
    for linha in range (FUNDO_LINHAS):
        for coluna in range (FUNDO_COLUNAS):
            fundo[linha][coluna] = 0

linhas()

jogador = 1
fim_de_jogo = False

#loop_principal
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not fim_de_jogo:
            mouseX = event.pos[0]
            mouseY = event.pos[1]

            linha_clique = int(mouseY // 200)
            coluna_clique = int(mouseX // 200)

            if quadrados_disponiveis(linha_clique, coluna_clique):
                quadrado_marcado(linha_clique, coluna_clique, jogador)
                if ganhar(jogador):
                    fim_de_jogo = True
                jogador = jogador % 2 + 1


                desenha_figuras()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart()
                fim_de_jogo = False

    pygame.display.update()