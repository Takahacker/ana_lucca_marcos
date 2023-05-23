import pygame
import random

# Inicialização do Pygame
pygame.init()

# ----- Configurações da tela
WIDTH = 600
HEIGHT = 400
altura = 50

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Jogo dos Peixes')

# ----- Configurações dos objetos do jogo
player_image = pygame.image.load('player.png')
agua_viva_small = pygame.image.load('agua_viva_small.png')
tubarao_grande = pygame.image.load('tubarao_grande.png')
background = pygame.image.load('background.png')

font = pygame.font.Font(None, 36)
score1 = 0
score2 = 0

# ----- Definição das classes
class Player(pygame.sprite.Sprite):
    def __init__(self, image, keys):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

        self.image = image
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
    def __init__(self, image):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = random.randint(altura, HEIGHT - altura)
        self.speedx = random.randint(2, 4)
        self.speedy = 0

    def update(self):
        # Atualizando a posição do peixe
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        # Se o peixe passar do final da tela, volta para cima e sorteia
        # novas posições e velocidades
        if self.rect.bottom > HEIGHT or self.rect.right < 0:
            self.rect.x = 0
            self.rect.y = random.randint(altura, HEIGHT - altura)
            self.speedx = random.randint(2, 4)
            self.speedy = 0

# ----- Criação de objetos
player1 = Player(player_image, {'up': pygame.K_w, 'down': pygame.K_s, 'left': pygame.K_a, 'right': pygame.K_d})
player2 = Player(player_image, {'up': pygame.K_UP, 'down': pygame.K_DOWN, 'left': pygame.K_LEFT, 'right': pygame.K_RIGHT})
peixe1 = Peixe(agua_viva_small)
peixe2 = Peixe(tubarao_grande)

# ----- Criação dos grupos
all_sprites = pygame.sprite.Group()
all_sprites.add(player1, player2, peixe1, peixe2)

all_peixes = pygame.sprite.Group()
all_peixes.add(peixe1, peixe2)

# ----- Loop principal
game = True
clock = pygame.time.Clock()
FPS = 30

while game:
    clock.tick(FPS)

    # Trata eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False

    # Atualiza estado do jogo
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
    if player1.rect.top <= altura:
        score1 += 1
        player1.rect.centerx = WIDTH / 3
        player1.rect.bottom = HEIGHT - 8

    if player2.rect.top <= altura:
        score2 += 1
        player2.rect.centerx = WIDTH / 2
        player2.rect.bottom = HEIGHT - 15

    # Gera saídas
    window.fill((0, 0, 0))
    window.blit(background, (0, 0))

    all_peixes.draw(window)
    all_sprites.draw(window)

    # Exibe a pontuação na tela
    score1_text = font.render("Jogador 1: " + str(score1), True, (255, 255, 255))
    window.blit(score1_text, (10, 10))
    score2_text = font.render("Jogador 2: " + str(score2), True, (255, 255, 255))
    window.blit(score2_text, (250, 10))

    pygame.display.update()

# Finalização
pygame.quit()
