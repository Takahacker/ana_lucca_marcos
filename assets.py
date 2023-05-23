import pygame
import os
from configuracoes import WIDTH, HEIGHT, largura, altura, larg_tub, alt_tub

FONTE = 'font'
BACKGROUND = 'background'
AGUA_VIVA = 'agua_viva'
TUBARAO = 'tubarao' 
JOGADOR = 'player_image'

def load_assets():
    imagens = {}
    imagens[FONTE] = pygame.font.SysFont(None, 48)
    imagens[BACKGROUND] = pygame.image.load('imagens/BACKGROUND.png').convert()
    imagens[AGUA_VIVA] = pygame.image.load('imagens/aguaviva_png.png').convert_alpha()
    imagens[AGUA_VIVA] = pygame.transform.scale(imagens['agua_viva'], (largura, altura))
    imagens[TUBARAO] = pygame.image.load('imagens/shark03.png').convert_alpha()
    imagens[TUBARAO] = pygame.transform.scale(imagens['tubarao'], (larg_tub, alt_tub))
    imagens[JOGADOR] = pygame.image.load('imagens/bob_esponja_direita.png').convert_alpha()
    imagens[JOGADOR] = pygame.transform.scale(imagens['player_image'], (largura, altura))

    return imagens