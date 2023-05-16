'''Utilize uma janela de 600 X 300 pixels;
Mude o título para Jogo da/do NOME (onde NOME é o seu nome);
Mude a cor da janela para azul ao invés de branco;
Faça o jogo fechar assim que o usuário apertar qualquer tecla do teclado. Dica: procure pelo evento pygame.KEYUP.'''
import pygame

pygame.init()

window = pygame.display.set_mode((600,300))
pygame.display.set_caption("Ana Clara")

game = True

while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False

    window.fill((176,224,230))

    pygame.display.update()

pygame.quit()