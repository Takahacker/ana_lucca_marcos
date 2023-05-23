import random
import pygame
from configuracoes import WIDTH, HEIGHT, largura, altura, larg_tub, alt_tub
from assets import FONTE, BACKGROUND, AGUA_VIVA, TUBARAO, BOB_ESPONJA,  PATRICK

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