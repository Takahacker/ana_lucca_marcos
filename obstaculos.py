# ===== Inicialização =====
# ----- Importa e inicia pacotes
import pygame
import random

pygame.init()

# ----- Gera tela principal
WIDTH = 600
HEIGHT = 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Crossy Ocean')

# ----- Inicia assets
largura = 50
altura = 38
larg_tub = 130
alt_tub = 90
font = pygame.font.SysFont(None, 48)
background = pygame.image.load('imagens/fundo_mario.jpg').convert()



peixe1 = pygame.image.load('imagens/peixe1.png').convert_alpha()
peixe1_small = pygame.transform.scale(peixe1, (largura, altura))

tubarao = pygame.image.load('imagens/tubarao.png').convert_alpha()
tubarao_grande = pygame.transform.scale(tubarao, (larg_tub, alt_tub))



lista_y = []
lista_x = []
lista_larg = []
velocidade_peixes_x= []

# ----- Inicia estruturas de dados

game = True

class Peixe(pygame.sprite.Sprite):
    def __init__(self, imgagens):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

        self.image = imgagens
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = random.randint(-100, -altura)
        self.speedx = -1
        self.speedy = 0

    def update(self):
        # Atualizando a posição do meteoro
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        # Se o peixe passar do final da tela, volta para cima e sorteia
        # novas posições e velocidades
        if self.rect.top > HEIGHT or self.rect.right < 0 or self.rect.left > WIDTH:
            self.rect.x = 0
            self.rect.y = random.randint(-100, HEIGHT - altura)
            self.speedx = random.randint(0, 4)
            self.speedy = 0


all_peixes = pygame.sprite.Group()

for i in range(8):
    peixe1 = Peixe(peixe1_small)
    all_peixes.add(peixe1)
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
    # Atualizando a posição dos peixes
    for peixe in all_peixes:
        peixe.update()

    # ----- Gera saídas
    window.fill((0, 0, 0))  # Preenche com a cor branca
    window.blit(background, (0, 0))
    # Desenhando meteoros
    all_peixes.draw(window)

    pygame.display.update()  # Mostra o novo frame para o jogador

# ===== Finalização =====
pygame.quit()  # Função do PyGame que finaliza os recursos utilizados