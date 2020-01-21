import pygame
from utils.load import *

class Buffalo(pygame.sprite.Sprite):

    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image('Buffalo.png', -1)
        self.image = pygame.transform.scale(self.image, (int(width), int(height)))
        self.rect = self.image.get_rect().move(int(x),int(y))

    def draw(self, surface):
        surface.blit(self.image, self.rect)