import pygame
from random import randint, choice, random


class Food(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.Surface((5, 5))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(midbottom=(x, y))
