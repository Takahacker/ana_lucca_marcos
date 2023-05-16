import pygame

pygame.init()

window = pygame.display.set_mode((500, 400))
pygame.display.set_caption('Bandeira do Brasil')

game = True

while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False

    window.fill((0, 128, 52))
      # Preenche a janela com branco

    # Desenha o losango amarelo da bandeira
    cor_amarelo = (252, 209, 22)
    vertices_losango = [(250, 0), (500, 200), (250, 400), (0, 200)]
    pygame.draw.polygon(window, cor_amarelo, vertices_losango)

    # Desenha o círculo verde da bandeira
    cor_verde = (0, 85, 164)
    centro_circulo = (250, 200)
    raio_circulo = 90
    pygame.draw.circle(window, cor_verde, centro_circulo, raio_circulo)

    pygame.display.update()

pygame.quit()
