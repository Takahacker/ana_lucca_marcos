import threading
import tkinter as tk
import pygame

# Função que será executada na nova thread
def run_pygame():
    # Inicialização do Pygame
    pygame.init()

    # Configurações da janela em Pygame
    largura = 800
    altura = 600
    janela = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption("Botão de Reprodução")

    # Cores em Pygame
    BRANCO = (255, 255, 255)
    VERDE = (0, 255, 0)

    # Posição e dimensões do botão em Pygame
    botao_largura = 100
    botao_altura = 100
    botao_posicao_x = (largura - botao_largura) // 2
    botao_posicao_y = (altura - botao_altura) // 2

    # Variável para verificar se o botão está pressionado em Pygame
    botao_clicado = False

    # Loop principal do jogo em Pygame
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

        # Desenha o botão em Pygame
        pygame.draw.rect(janela, VERDE, (botao_posicao_x, botao_posicao_y, botao_largura, botao_altura))
        if not botao_clicado:
            pygame.draw.polygon(janela, BRANCO, [(botao_posicao_x + 30, botao_posicao_y + 20),
                                                  (botao_posicao_x + 30, botao_posicao_y + 80),
                                                  (botao_posicao_x + 80, botao_posicao_y + 50)])

        pygame.display.update()

    # Encerrando o Pygame
    pygame.quit()

# Função que será executada quando o botão de executar for clicado em Tkinter
def executar_codigo():
    # Cria a nova thread para executar o Pygame
    thread_pygame = threading.Thread(target=run_pygame)
    thread_pygame.start()

# Cria uma instância da janela principal em Tkinter
janela = tk.Tk()

# Configurações da janela em Tkinter
janela.title("Tela de Execução")
janela.geometry("400x300")

# Botão para executar o código em Tkinter
botao_executar = tk.Button(janela, text="Executar", command=executar_codigo)
botao_executar.pack()

# Loop principal da janela em Tkinter
janela.mainloop()
