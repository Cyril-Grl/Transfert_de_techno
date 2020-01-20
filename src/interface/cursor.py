import pygame
from utils.load import *

class Cursor(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)        #Appel du constructeur de Sprite
        self.image = load_image('brawnBucket.png', -1)
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self._selected = False
        self._quantity = 0

    def update(self):
        pos = pygame.mouse.get_pos()
        self.rect.midtop = pos

    def printQuantity(self):
        self.image = load_image('brawnBucket.png', -1)
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        font = pygame.font.Font(None, 30)
        text = font.render(str(self._quantity),1,(10, 10, 10))
        textpos = self.image.get_rect().center
        self.image.blit(text, textpos)

    def fillCursorBucket(self, target):
        if not self._selected:
            hitbox = self.rect.inflate(-5, -5)
            return hitbox.colliderect(target.rect)

    def emptyCursorBucket(self, target):
        if self._selected:
            hitbox = self.rect.inflate(-5, -5)
            return hitbox.colliderect(target.rect)

    @property
    def selected(self):
        return self._selected
    
    @selected.setter
    def selected(self, selected):
        self._selected = selected

    @property
    def quantity(self):
        return self._quantity
    
    @quantity.setter
    def quantity(self, quantity):
        self._quantity = quantity