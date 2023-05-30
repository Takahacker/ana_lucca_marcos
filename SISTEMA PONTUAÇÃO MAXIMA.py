import pygame
import random
import time
import json

pygame.mixer.init()
pygame.init()


# ----- Gera tela principal
WIDTH = 600
HEIGHT = 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (255,0,0)

# Carregar o dicionário de jogadores existente do arquivo JSON, se houver
try:
    with open("players.json", "r") as file:
        players = json.load(file)
except FileNotFoundError:
    players = {}

player_name = ""

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
pygame.mixer.music.set_volume(0.4)
musica = pygame.mixer.Sound('musica.mp3')
som_agua_viva = pygame.mixer.Sound('somag.mp3')
boom = pygame.mixer.Sound('boom.mp3')
heheheha = pygame.mixer.Sound('heheheha.mp3')

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
image = pygame.image.load('imagens/entrada.jpeg').convert()
image = pygame.transform.scale(image,(WIDTH,HEIGHT))

# Variável para verificar se o botão está pressionado em Pygame
botao_clicado = False
nomes_colocados = 0
nomes_jogadores = []
#loop da tela de entrada
executando = True
while executando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            executando = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_RETURN:
                # Quando o jogador pressionar Enter, adicionar o nome e pontuação ao dicionário de jogadores
                nomes_jogadores.append(player_name)
                nomes_colocados += 1
                if player_name:
                    with open("players.json", "r") as file:
                        conteudo = file.read()
                    dados = json.loads(conteudo)
                    for player in dados:
                        if player == player_name:
                            player_score = dados[player]
                    if player_name not in dados:
                        dados[player_name] = 0
                    with open("players.json", "w") as file:
                        json.dump(dados, file)
                    player_name = ""
                if nomes_colocados == 2:
                    nomes_colocados = 0
                    botao_clicado = True
            elif evento.key == pygame.K_BACKSPACE:
                # Quando o jogador pressionar Backspace, remover o último caractere do nome
                player_name = player_name[:-1]
            elif evento.key == pygame.K_UP:
                # Quando o jogador pressionar a seta para cima, aumentar a pontuação
                player_score += 1
            elif evento.key == pygame.K_DOWN:
                # Quando o jogador pressionar a seta para baixo, diminuir a pontuação (mínimo de 0)
                player_score = max(0, player_score - 1)
            else:
                # Adicionar o caractere digitado ao nome do jogador
                player_name += evento.unicode

    # Desenha o botão em Pygame
    janela.blit(image, (0, 1))

    if nomes_colocados == 0:
        text = font.render("Nome do jogador 1: " + player_name, True, BRANCO)

    elif nomes_colocados == 1:
        text = font.render("Nome do jogador 2: " + player_name, True, BRANCO)

    text_rect = text.get_rect(center=(300, 550))
    window.blit(text, text_rect)
    if not botao_clicado:
        pygame.display.update()
    else:

        nome_jogador1 = nomes_jogadores[0]
        nome_jogador2 = nomes_jogadores[1]
        clock = pygame.time.Clock()
        #atualiza a tela 60 vezes por segundo
        FPS = 60
        current_time = 0
        tempo = 0
        start_time = time.time()
        time_started = False
        tempo_restante = 0

        # ===== Loop principal =====
        musica.play()
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
                boom.play()
                heheheha.play()
                player1.rect.centerx = WIDTH / 3
                player1.rect.bottom = HEIGHT - 8
                score1 = 0

            if pygame.sprite.spritecollide(player2, all_tubaroes, False):
                boom.play()
                heheheha.play()
                player2.rect.centerx = WIDTH / 2
                player2.rect.bottom = HEIGHT - 15
                score2 = 0
            
            if pygame.sprite.spritecollide(player1, all_aguas_vivas, True):
                som_agua_viva.play()
                score1 += 1
                agua_viva1 = AGUA_VIVA(agua_viva_small)
                all_aguas_vivas.add(agua_viva1)

            if pygame.sprite.spritecollide(player2, all_aguas_vivas, True):
                som_agua_viva.play()
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
            score1_text = font.render(f"{nome_jogador1}: " + str(score1), True, (BRANCO))
            window.blit(score1_text, (10, 10))
            score2_text = font.render(f"{nome_jogador2}: " + str(score2), True, (BRANCO))
            window.blit(score2_text, (10, 50))


            if time_started:

                tempo_restante = 60-current_time
                tempo_text = font.render("Tempo restante: {0:.0f}".format((tempo_restante)), True, (255,255,255))
                window.blit(tempo_text, (270, 10)) 

                if current_time >= 60:
                    game = False
                    executando = False 

            pygame.display.update()

#atualiza arquivo com as pontuacoes
with open('players.json', 'r') as file:
    conteudo = file.read()
dados = json.loads(conteudo)
for player in dados:
    if player == nome_jogador1:
        if score1 > dados[nome_jogador1]:
            dados[nome_jogador1] = score1
    elif player == nome_jogador2:
        if score2 > dados[nome_jogador2]:
            dados[nome_jogador2] = score2
high_score = max(dados.values())
for player,pontuacao in dados.items():
    if pontuacao == high_score:
        best_player = player

with open('players.json', 'w') as file:
    json.dump(dados, file)

pygame.mixer.stop()

highscore_text = font.render("Pontuação máxima:", True, (PRETO))
bestplayer_text = font.render(f"{best_player} --> {high_score}", True, (PRETO))
tela_final = True
while tela_final:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            tela_final = False
    if score1>score2:
        window.fill((0, 0, 0))  # Preenche com a cor preta
        bob_text = font.render(f"{nome_jogador1} venceu! ", True, (PRETO))
        window.blit(background_bob, (0, 0)) 
        window.blit(bob_text, (10, 10))
        window.blit(highscore_text, (10, 450))
        window.blit(bestplayer_text, (10, 500))                
    elif score2>score1:
        window.fill((0, 0, 0))  # Preenche com a cor preta
        pat_text = font.render(f"{nome_jogador2} venceu! ", True, (PRETO))
        window.blit(background_patrick, (0, 0))
        window.blit(pat_text, (10, 10))
        window.blit(highscore_text, (270, 10))
        window.blit(bestplayer_text, (270, 60)) 
    else:
        window.fill((0, 0, 0))  # Preenche com a cor preta
        highscore_text = font.render("Pontuação máxima:", True, (BRANCO))
        bestplayer_text = font.render(f"{best_player} --> {high_score}", True, (BRANCO))
        holandes_text = font.render("O holandes voador venceu =( ", True, (BRANCO))
        window.blit(background_holandes, (0, 0))
        window.blit(holandes_text, (10, 10))
        window.blit(highscore_text, (100, 500))
        window.blit(bestplayer_text, (100, 550))   

    pygame.display.update()