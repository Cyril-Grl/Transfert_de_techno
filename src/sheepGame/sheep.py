import pygame
from utils.load import *

class Sheep(pygame.sprite.Sprite):

    def __init__(self, x, y, width, height, sheep):
        pygame.sprite.Sprite.__init__(self)

        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._mouse_over = False
        self._sheep = sheep
        self._mouse_up_right = False
        self._mouse_up_left = False

        if sheep:
            default_image = load_image('sheepWhite.png', -1)
        else:
            default_image = load_image('goat.png', -1)

        default_image = pygame.transform.scale(default_image, (int(width), int(height)))
        highlighted_image = default_image.copy()
        pygame.draw.rect(highlighted_image, (255,0,0), (0, 0, int(self._width), int(self._height)), 2)

        self.images = [default_image, highlighted_image]

        self.rects = [
            default_image.get_rect().move(int(x),int(y)),
            highlighted_image.get_rect().move(int(x),int(y)),
        ]

    @property
    def image(self):
        return self.images[1] if self._mouse_over else self.images[0]

    @property
    def rect(self):
        return self.rects[1] if self._mouse_over else self.rects[0]

    def update(self, mouse_pos, mouse_up_right, mouse_up_left):
        if self.rect.collidepoint(mouse_pos):
            self._mouse_over = True
            
            if mouse_up_right:
                self._mouse_up_right = True
                return True

            if mouse_up_left:
                self._mouse_up_left = True
                return True
        else:
            self._mouse_over = False
            return False

    def moveBeast(self):
        if self._sheep and self._mouse_up_left:
            self.rects[0] = self.images[0].get_rect().move(int(self._x - self._width), int(self._y))
            self.rects[1] = self.images[1].get_rect().move(int(self._x - self._width), int(self._y))
            self._mouse_up_left = False
        elif self._sheep and self._mouse_up_right:
            self.rects[0] = self.images[0].get_rect().move(int(self._x + self._width), int(self._y))
            self.rects[1] = self.images[1].get_rect().move(int(self._x + self._width), int(self._y))
            self._mouse_up_right = False
        elif not self._sheep and self._mouse_up_left:
            self.rects[0] = self.images[0].get_rect().move(int(self._x - self._width), int(self._y))
            self.rects[1] = self.images[1].get_rect().move(int(self._x - self._width), int(self._y))
            self._mouse_up_left = False
        elif not self._sheep and self._mouse_up_right:
            self.rects[0] = self.images[0].get_rect().move(int(self._x + self._width), int(self._y))
            self.rects[1] = self.images[1].get_rect().move(int(self._x + self._width), int(self._y))
            self._mouse_up_right = False

    def draw(self, surface):
        surface.blit(self.image, self.rect)