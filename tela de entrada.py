import pygame
import random

    
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
score1 = 0
score2 = 0
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
    else:

        pygame.init()

        # ----- Gera tela principal
        WIDTH = 600
        HEIGHT = 600
        window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Crossy Ocean')

        # ----- Inicia assets
        largura = 60
        altura = 60
        larg_tub = 130
        alt_tub = 90
        font = pygame.font.SysFont('imagens/Fontes/retro_mario/RetroMario-Regular.otf', 48)
        background = pygame.image.load('imagens/fundo_mario.jpg').convert()

        agua_viva = pygame.image.load('imagens/aguaviva_png.png').convert_alpha()
        agua_viva_small = pygame.transform.scale(agua_viva, (largura, altura))

        tubarao = pygame.image.load('imagens/shark03.png').convert_alpha()
        tubarao_grande = pygame.transform.scale(tubarao, (larg_tub, alt_tub))

        player_image = pygame.image.load('imagens/bob_esponja_direita.png').convert_alpha()
        player_image = pygame.transform.scale(player_image, (largura, altura))

        # ----- Inicia estruturas de dados
        game = True
        score = 0

        class Player(pygame.sprite.Sprite):
            def __init__(self, imagens, keys):
                # Construtor da classe mãe (Sprite).
                pygame.sprite.Sprite.__init__(self)

                self.image = imagens
                self.rect = self.image.get_rect()
                self.rect.centerx = WIDTH / 2
                self.rect.bottom = HEIGHT - 10
                self.speedx = 0
                self.speedy = 0
                self.keys = keys

            def update(self):
                # Atualização da posição do jogador
                keys = pygame.key.get_pressed()
                if keys[self.keys['up']]:
                    self.speedy = -3
                    self.speedx = 0
                elif keys[self.keys['down']]:
                    self.speedy = 3
                    self.speedx = 0
                else:
                    self.speedy = 0

                if keys[self.keys['left']]:
                    self.speedx = -3
                    self.speedy = 0
                elif keys[self.keys['right']]:
                    self.speedx = 3
                    self.speedy = 0
                else:
                    self.speedx = 0

                self.rect.x += self.speedx
                self.rect.y += self.speedy

                # Mantém dentro da tela
                if self.rect.right > WIDTH:
                    self.rect.right = WIDTH
                if self.rect.left < 0:
                    self.rect.left = 0
                if self.rect.bottom > HEIGHT:
                    self.rect.bottom = HEIGHT
                if self.rect.top < 0:
                    self.rect.top = 0

        class Peixe(pygame.sprite.Sprite):
            def __init__(self, imgagens):
                # Construtor da classe mãe (Sprite).
                pygame.sprite.Sprite.__init__(self)

                self.image = imgagens
                self.rect = self.image.get_rect()
                self.rect.x = 0
                self.rect.y = random.randint(-100, -altura)
                self.speedx = 2
                self.speedy = 0

            def update(self):
                # Atualizando a posição do peixe
                self.rect.x += self.speedx
                self.rect.y += self.speedy

                # Se o peixe passar do final da tela, volta para cima e sorteia
                # novas posições e velocidades
                if self.rect.top < 0 or self.rect.bottom > HEIGHT or self.rect.right < 0 or self.rect.left > WIDTH:
                    self.rect.x = 0
                    self.rect.y = random.randint(-100, HEIGHT - altura)
                    self.speedx = random.randint(2, 4)
                    self.speedy = 0

        # ----- Criação de objetos
        player1 = Player(player_image, {'up': pygame.K_w, 'down': pygame.K_s, 'left': pygame.K_a, 'right': pygame.K_d})
        player2 = Player(player_image, {'up': pygame.K_t, 'down': pygame.K_g, 'left': pygame.K_f, 'right': pygame.K_h})

        all_peixes = pygame.sprite.Group()
        all_sprites = pygame.sprite.Group()

        # Adiciona jogadores ao grupo de sprites
        all_sprites.add(player1)
        player1.rect.centerx = WIDTH / 3
        player1.rect.bottom = HEIGHT - 8

        all_sprites.add(player2)
        player2.rect.centerx = WIDTH / 2
        player2.rect.bottom = HEIGHT - 12

        for i in range(6):
            peixe1 = Peixe(agua_viva_small)
            all_peixes.add(peixe1)

        for i in range(4):
            tubarao = Peixe(tubarao_grande)
            all_peixes.add(tubarao)

        clock = pygame.time.Clock()
        FPS = 30

        # ===== Loop principal =====
        while game:
            clock.tick(FPS)
            
            # ----- Trata eventos
            for event in pygame.event.get():
                # ----- Verifica consequências
                if event.type == pygame.QUIT:
                    game = False

            # ----- Atualiza estado do jogo
            all_sprites.update()

            # Verifica colisão entre os jogadores e os obstáculos
            if pygame.sprite.spritecollide(player1, all_peixes, False):
                player1.rect.centerx = WIDTH / 3
                player1.rect.bottom = HEIGHT - 8

            if pygame.sprite.spritecollide(player2, all_peixes, False):
                player2.rect.centerx = WIDTH / 2
                player2.rect.bottom = HEIGHT - 15

            for peixe in all_peixes:
                peixe.update()

            # Verifica se jogador encostou na parte superior da tela
            if player1.rect.top <= 0:
                score1 += 1
                player1.rect.centerx = WIDTH / 3
                player1.rect.bottom = HEIGHT - 8

            if player2.rect.top <= 0:
                score2 += 1
                player2.rect.centerx = WIDTH / 2
                player2.rect.bottom = HEIGHT - 15

            # ----- Gera saídas
            window.fill((0, 0, 0))  # Preenche com a cor preta
            window.blit(background, (0, 0))

            all_peixes.draw(window)
            all_sprites.draw(window)

            # Exibe a pontuação na tela
            score1_text = font.render("Jogador 1: " + str(score1 ), True, (255, 255, 255))
            window.blit(score1_text, (10, 10))
            score2_text = font.render("Jogador 2: " + str(score2), True, (255, 255, 255))
            window.blit(score2_text, (250, 10))

            pygame.display.update()

        # ===== Finalização =====
        pygame.quit()  # Função do PyGame que finaliza os recursos utilizados

    pygame.display.update()

# Encerrando o Pygame
pygame.quit()