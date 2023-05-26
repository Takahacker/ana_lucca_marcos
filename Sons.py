import pygame
import random
import time

pygame.mixer.init()
pygame.init()


# ----- Gera tela principal
WIDTH = 600
HEIGHT = 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Crossy Ocean')

# ----- Inicia assets
largura_agua_viva = 60
altura_agua_viva = 60
largura_player = 80
altura_player = 80
larg_tub = 130
alt_tub = 90
font = pygame.font.SysFont('imagens/Fontes/retro_mario/RetroMario-Regular.otf', 48)
font_small = pygame.font.SysFont('imagens/Fontes/retro_mario/RetroMario-Regular.otf', 24)
background = pygame.image.load('imagens/Image nova.jpg').convert()
background = pygame.transform.scale(background,(WIDTH,HEIGHT))

background_bob = pygame.image.load('imagens/ganhador1.jpeg').convert()
background_bob = pygame.transform.scale(background_bob,(WIDTH,HEIGHT))
background_patrick = pygame.image.load('imagens/ganhador2.jpeg').convert()
background_patrick = pygame.transform.scale(background_patrick,(WIDTH,HEIGHT))
background_holandes = pygame.image.load('imagens/holandes_ganhador.jpeg').convert()
background_holandes = pygame.transform.scale(background_holandes,(WIDTH,HEIGHT))

agua_viva = pygame.image.load('imagens/AGUAVIVA.png').convert_alpha()
agua_viva_small = pygame.transform.scale(agua_viva, (largura_agua_viva, altura_agua_viva))

tubarao = pygame.image.load('imagens/holandes.png').convert_alpha()
tubarao_grande = pygame.transform.scale(tubarao, (larg_tub, alt_tub))

player_image1 = pygame.image.load('imagens/bob_esponja_com_rede.png').convert_alpha()
player_image1 = pygame.transform.scale(player_image1, (largura_player, altura_player))

player_image2 = pygame.image.load('imagens/patrick_com_rede.png').convert_alpha()
player_image2 = pygame.transform.scale(player_image2, (largura_player, altura_player))

# Carrega os sons do jogo
pygame.mixer.music.load('assets/snd/tgfcoder-FrozenJam-SeamlessLoop.ogg')
pygame.mixer.music.set_volume(0.4)
# ----- Inicia estruturas de dados
game = True
score1 = 0
score2 = 0

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
            self.speedy = -5
            self.speedx = 0
        elif keys[self.keys['down']]:
            self.speedy = 5
            self.speedx = 0
        else:
            self.speedy = 0

        if keys[self.keys['left']]:
            self.speedx = -5
            self.speedy = 0
        elif keys[self.keys['right']]:
            self.speedx = 5
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

class AGUA_VIVA(pygame.sprite.Sprite):
    def __init__(self, imgagens):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

        self.image = imgagens
        self.rect = pygame.Rect(0, 0, largura_agua_viva, altura_agua_viva)
        self.rect.x = random.randint(-100,-50)
        self.rect.bottom = random.randint(0, HEIGHT-100)
        self.speedx = random.randint(2, 6)
        self.speedy = 0

    def update(self):
        # Atualizando a posição do peixe
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        # Se o peixe passar do final da tela, volta para cima e sorteia
        # novas posições e velocidades
        if self.rect.top < 0 or self.rect.bottom > HEIGHT or self.rect.left > WIDTH:
            self.rect.x = -100
            self.rect.bottom = random.randint(0, HEIGHT-100)
            self.speedx = random.randint(2, 6)
            self.speedy = 0

class HOLANDES(pygame.sprite.Sprite):
    def __init__(self, imgagens):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

        self.image = imgagens
        self.rect = pygame.Rect(0, 0, 110, 65)
        self.rect.x = random.randint(-100,-50)
        self.rect.bottom = random.randint(0, HEIGHT-100)
        self.speedx = random.randint(2, 6)
        self.speedy = 0

    def update(self):
        # Atualizando a posição do peixe
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        # Se o peixe passar do final da tela, volta para cima e sorteia
        # novas posições e velocidades
        if self.rect.top < 0 or self.rect.bottom > HEIGHT or self.rect.left > WIDTH:
            self.rect.x = -100
            self.rect.bottom = random.randint(0, HEIGHT-100)
            self.speedx = random.randint(2, 6)
            self.speedy = 0

# ----- Criação de objetos
player1 = Player(player_image1, {'up': pygame.K_w, 'down': pygame.K_s, 'left': pygame.K_a, 'right': pygame.K_d})
player2 = Player(player_image2, {'up': pygame.K_UP, 'down': pygame.K_DOWN, 'left': pygame.K_LEFT, 'right': pygame.K_RIGHT})

all_tubaroes = pygame.sprite.Group()
all_aguas_vivas = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

# Adiciona jogadores ao grupo de sprites
all_sprites.add(player1)
player1.rect.centerx = WIDTH / 3
player1.rect.bottom = HEIGHT - 8

all_sprites.add(player2)
player2.rect.centerx = WIDTH / 2
player2.rect.bottom = HEIGHT - 12

for i in range(6):
    agua_viva1 = AGUA_VIVA(agua_viva_small)
    all_aguas_vivas.add(agua_viva1)

for i in range(2):
    tubarao = HOLANDES(tubarao_grande)
    all_tubaroes.add(tubarao)

clock = pygame.time.Clock()
FPS = 60

# Configurações da janela em Pygame
janela = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Botão de Reprodução")

#tela de entrada
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
image = pygame.image.load('imagens/entrada.jpeg').convert()
image = pygame.transform.scale(image,(WIDTH,HEIGHT))
estamos = font_small.render("Aperte", True, BRANCO)
capitao = font_small.render("para jogar", True, BRANCO)
# Posição e dimensões do botão em Pygame
botao_largura = 100
botao_altura = 100
botao_posicao_x = 400
botao_posicao_y = 130


# Variável para verificar se o botão está pressionado em Pygame
botao_clicado = False

#loop da tela de entrada
executando = True
while executando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            executando = False
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if botao_posicao_x <= pygame.mouse.get_pos()[0] <= botao_posicao_x + botao_largura \
                    and botao_posicao_y <= pygame.mouse.get_pos()[1] <= botao_posicao_y + botao_altura:
                botao_clicado = True


    # Desenha o botão em Pygame
    janela.blit(image, (0, 1))
    pygame.draw.rect(janela, PRETO, (botao_posicao_x, botao_posicao_y, botao_largura, botao_altura))
    if not botao_clicado:
        janela.blit(estamos,(botao_posicao_x + 12, botao_posicao_y + 25))
        janela.blit(capitao,(botao_posicao_x + 12, botao_posicao_y + 55))
        pygame.display.update()
    else:

        clock = pygame.time.Clock()
        #atualiza a tela 60 vezes por segundo
        FPS = 60
        current_time = 0
        tempo = 0
        start_time = time.time()
        time_started = False
        tempo_restante = 0

        # ===== Loop principal =====
        while game:
            
            clock.tick(FPS)

            current_time = time.time() - start_time
            
            if current_time>=1 and not time_started:
                time_started = True
                start_time = time.time()
            
            # ----- Trata eventos
            for event in pygame.event.get():
                # ----- Verifica consequências
                if event.type == pygame.QUIT:
                    game = False

            # ----- Atualiza estado do jogo
            all_sprites.update()

            # Verifica colisão entre os jogadores e os obstáculos
            if pygame.sprite.spritecollide(player1, all_tubaroes, False):
                player1.rect.centerx = WIDTH / 3
                player1.rect.bottom = HEIGHT - 8
                score1 = 0

            if pygame.sprite.spritecollide(player2, all_tubaroes, False):
                player2.rect.centerx = WIDTH / 2
                player2.rect.bottom = HEIGHT - 15
                score2 = 0
            
            if pygame.sprite.spritecollide(player1, all_aguas_vivas, True):
                score1 += 1
                agua_viva1 = AGUA_VIVA(agua_viva_small)
                all_aguas_vivas.add(agua_viva1)

            if pygame.sprite.spritecollide(player2, all_aguas_vivas, True):
                score2 += 1
                agua_viva1 = AGUA_VIVA(agua_viva_small)
                all_aguas_vivas.add(agua_viva1)

            for tubarao in all_tubaroes:
                tubarao.update()
            
            for aguaviva in all_aguas_vivas:
                aguaviva.update()

            # ----- Gera saídas
            window.fill((0, 0, 0))  # Preenche com a cor preta
            window.blit(background, (0, 0))

            all_tubaroes.draw(window)
            all_aguas_vivas.draw(window)
            all_sprites.draw(window)

            # Exibe a pontuação na tela
            score1_text = font.render("Jogador 1: " + str(score1), True, (BRANCO))
            window.blit(score1_text, (10, 10))
            score2_text = font.render("Jogador 2: " + str(score2), True, (BRANCO))
            window.blit(score2_text, (10, 50))


            if time_started:

                tempo_restante = 60-current_time
                tempo_text = font.render("Tempo restante: {0:.0f}".format((tempo_restante)), True, (255,255,255))
                window.blit(tempo_text, (270, 10)) 

                if current_time >= 60:
                    game = False
                    executando = False 

            pygame.display.update()

tela_final = True
while tela_final:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            tela_final = False
    if score1>score2:
        window.fill((0, 0, 0))  # Preenche com a cor preta
        bob_text = font.render("Jogador 1 venceu! ", True, (PRETO))
        window.blit(background_bob, (0, 0)) 
        window.blit(bob_text, (10, 10))                   
    elif score2>score1:
        window.fill((0, 0, 0))  # Preenche com a cor preta
        pat_text = font.render("Jogador 2 venceu! ", True, (PRETO))   
        window.blit(background_patrick, (0, 0))
        window.blit(pat_text, (10, 10))
    else:
        window.fill((0, 0, 0))  # Preenche com a cor preta
        holandes_text = font.render("O holandes voador venceu =( ", True, (BRANCO))
        window.blit(background_holandes, (0, 0))
        window.blit(holandes_text, (10, 10))   

    pygame.display.update()