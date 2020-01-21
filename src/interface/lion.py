import pygame
from utils.load import *

class Lion(pygame.sprite.Sprite):

    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)

        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._mouse_over = False
        self._on_the_right = True
        self._on_the_left = False
        self._on_the_boat = False

        default_image = load_image('lion.png', -1)
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

    def update(self, mouse_pos, mouse_up):
        if self.rect.collidepoint(mouse_pos):
            self._mouse_over = True
            if mouse_up:
                if self._on_the_right and not self._on_the_boat:
                    self._on_the_boat = True
                    self.rects[0] = self.images[0].get_rect().move(int(self._width), int(self._y))
                    self.rects[1] = self.images[1].get_rect().move(int(self._width), int(self._y))
                elif self._on_the_left and not self._on_the_boat:
                    self._on_the_boat = True
                    self.rects[0] = self.images[0].get_rect().move(int(self._width), int(self._y))
                    self.rects[1] = self.images[1].get_rect().move(int(self._width), int(self._y))
                elif self._on_the_boat and self._on_the_right:
                    self._on_the_boat = False
                    self._on_the_right = False
                    self._on_the_left = True
                    self.rects[0] = self.images[0].get_rect().move(int(self._width * 2), int(self._y))
                    self.rects[1] = self.images[1].get_rect().move(int(self._width * 2), int(self._y))
                elif self._on_the_boat and self._on_the_left:
                    self._on_the_boat = False
                    self._on_the_right = True
                    self._on_the_left = False
                    self.rects[0] = self.images[0].get_rect().move(int(self._x), int(self._y))
                    self.rects[1] = self.images[1].get_rect().move(int(self._x), int(self._y))
        else:
            self._mouse_over = False

    def draw(self, surface):
        surface.blit(self.image, self.rect)