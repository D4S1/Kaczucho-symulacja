import pygame
from random import randint, choice, random


class Food(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.image.load('graphics/bug-light.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom=(x, y))
