import pygame
from utils.load import *

class Bucket(pygame.sprite.Sprite):

    def __init__(self, x, y, scale, s = 0, q = 0):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image('blueBucket.png', -1)
        self.image = pygame.transform.scale(self.image, (int(scale), int(y)))
        self.rect = self.image.get_rect().move(x,y)
        self._size = s
        self._quantity = q
        self._x = x
        self._y = y
        self._scale = scale
        self._selected = False
        self.printQuantity()
        #pygame.draw.rect(self.image, (255,0,0), (0, 0, int(scale), int(y)), 2)

    def printQuantity(self):
        self.image = load_image('blueBucket.png', -1)
        self.image = pygame.transform.scale(self.image, (int(self._scale), int(self._y)))
        self.rect = self.image.get_rect().move(self._x,self._y)
        font = pygame.font.Font(None, 30)
        text = font.render(str(str(self._quantity) + "/" + str(self._size)),1,(10, 10, 10))
        textpos = self.image.get_rect().center
        self.image.blit(text, textpos)
        if self._selected:
            pygame.draw.rect(self.image, (255,0,0), (0, 0, int(self._scale), int(self._y)), 2)

    @property
    def selected(self):
        return self._selected
    
    @selected.setter
    def selected(self, selected):
        self._selected = selected

    @property
    def size(self):
        return self._size
    
    @size.setter
    def size(self, size):
        self._size = size

    @property
    def quantity(self):
        return self._quantity
    
    @quantity.setter
    def quantity(self, quantity):
        self._quantity = quantity