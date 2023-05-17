import pygame

# Inicialização do Pygame
pygame.init()

# Configurações da janela
largura = 800
altura = 600
janela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Botão de Reprodução")

# Cores
BRANCO = (255, 255, 255)
VERDE = (0, 255, 0)

# Posição e dimensões do botão
botao_largura = 100
botao_altura = 100
botao_posicao_x = (largura - botao_largura) // 2
botao_posicao_y = (altura - botao_altura) // 2

# Variável para verificar se o botão está pressionado
botao_clicado = False

# Loop principal do jogo
executando = True
while executando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            executando = False
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if botao_posicao_x <= pygame.mouse.get_pos()[0] <= botao_posicao_x + botao_largura \
                    and botao_posicao_y <= pygame.mouse.get_pos()[1] <= botao_posicao_y + botao_altura:
                botao_clicado = True

    janela.fill(BRANCO)

    # Desenha o botão na tela
    pygame.draw.rect(janela, VERDE, (botao_posicao_x, botao_posicao_y, botao_largura, botao_altura))
    if not botao_clicado:
        pygame.draw.polygon(janela, BRANCO, [(botao_posicao_x + 30, botao_posicao_y + 20),
                                              (botao_posicao_x + 30, botao_posicao_y + 80),
                                              (botao_posicao_x + 80, botao_posicao_y + 50)])

    
    font = pygame.font.Font(None, 80)  # Define a fonte e o tamanho
    text = font.render("PYGAME", True, (0, 0, 0))  # Renderiza o texto
    text_rect = text.get_rect(center=(janela.get_width() // 2, janela.get_height() // 2 -100))  # Obtém o retângulo do texto
    janela.blit(text, text_rect)  # Desenha o texto na tela
    font = pygame.font.Font(None, 60)  # Define a fonte e o tamanho
    text = font.render("Início", True, (0, 0, 0))  # Renderiza o texto
    text_rect = text.get_rect(center=(janela.get_width() // 2, janela.get_height() // 2 + 100))  # Obtém o retângulo do texto
    janela.blit(text, text_rect)  # Desenha o texto na tela

    pygame.display.update()

# Encerrando o Pygame
pygame.quit()