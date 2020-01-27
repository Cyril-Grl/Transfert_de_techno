import pygame
from utils.load import *

class Sheep(pygame.sprite.Sprite):

    def __init__(self, x, y, width, height, sheep, position, screenWidth):
        pygame.sprite.Sprite.__init__(self)

        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._screen_width = screenWidth
        self._mouse_over = False
        self._mouse_up_right = False
        self._mouse_up_left = False
        self._position = position

        self._sheep = sheep

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

    @property
    def position(self):
        return self._position

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

    def moveBeast(self, etat):
        beastSide = False
        beastSideBySide = False
        if self._mouse_up_left and self._x > 0 and not self._sheep:
            for beast in etat:
                if(beast.position == self._position - 1):
                    beastSide = True
                if(beast.position == self._position - 2):
                    beastSideBySide = True      
            if not beastSide:
                self._x -= self._width
                self.rects[0] = self.images[0].get_rect().move(int(self._x), int(self._y))
                self.rects[1] = self.images[1].get_rect().move(int(self._x), int(self._y))
                self._position -= 1
            elif beastSide and not beastSideBySide and self._x - self._width * 2 >= 0:
                self._x -= self._width * 2
                self.rects[0] = self.images[0].get_rect().move(int(self._x), int(self._y))
                self.rects[1] = self.images[1].get_rect().move(int(self._x), int(self._y))
                self._position -= 2
        elif self._mouse_up_right and self._x < self._screen_width and self._sheep:
            for beast in etat:
                if(beast.position == self._position + 1):
                    beastSide = True
                if(beast.position == self._position + 2):
                    beastSideBySide = True
            if not beastSide:
                self._x += self._width
                self.rects[0] = self.images[0].get_rect().move(int(self._x), int(self._y))
                self.rects[1] = self.images[1].get_rect().move(int(self._x), int(self._y))
                self._position += 1
            elif beastSide and not beastSideBySide and self._x + self._width * 2 < self._screen_width:
                self._x += self._width * 2
                self.rects[0] = self.images[0].get_rect().move(int(self._x), int(self._y))
                self.rects[1] = self.images[1].get_rect().move(int(self._x), int(self._y))
                self._position += 2

        self._mouse_up_left = False
        self._mouse_up_right = False

    def draw(self, surface):
        surface.blit(self.image, self.rect)