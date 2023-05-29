import pygame
import json

pygame.init()

# Definir as cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Definir as dimensões da tela
WIDTH = 800
HEIGHT = 600

# Inicializar a tela
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Armazenamento de Nome e Pontuação")

# Carregar o dicionário de jogadores existente do arquivo JSON, se houver
try:
    with open("players.json", "r") as file:
        players = json.load(file)
except FileNotFoundError:
    players = {}

player_name = ""
player_score = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                # Quando o jogador pressionar Enter, adicionar o nome e pontuação ao dicionário de jogadores
                if player_name:
                    players[player_name] = player_score
                    with open("players.json", "w") as file:
                        json.dump(players, file)
                    player_name = ""
                    player_score = 0
            elif event.key == pygame.K_BACKSPACE:
                # Quando o jogador pressionar Backspace, remover o último caractere do nome
                player_name = player_name[:-1]
            elif event.key == pygame.K_UP:
                # Quando o jogador pressionar a seta para cima, aumentar a pontuação
                player_score += 1
            elif event.key == pygame.K_DOWN:
                # Quando o jogador pressionar a seta para baixo, diminuir a pontuação (mínimo de 0)
                player_score = max(0, player_score - 1)
            else:
                # Adicionar o caractere digitado ao nome do jogador
                player_name += event.unicode

    screen.fill(BLACK)
    font = pygame.font.Font(None, 36)
    text = font.render("Digite seu nome: " + player_name, True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    screen.blit(text, text_rect)
    score_text = font.render("Pontuação: " + str(player_score), True, WHITE)
    score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    screen.blit(score_text, score_rect)
    pygame.display.flip()

pygame.quit()