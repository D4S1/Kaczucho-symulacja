import pygame


class Button:

    def __init__(self, x, y, image):
        width = image.get_width()
        height = image.get_height()
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.pressed = False
        self.action = False

    def draw(self, screen):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.pressed:
                self.pressed = True

        if pygame.mouse.get_pressed()[0] == 0 and self.pressed:
            self.pressed = False
            self.action = not self.action

        screen.blit(self.image, (self.rect.x, self.rect.y))
        return self.action
