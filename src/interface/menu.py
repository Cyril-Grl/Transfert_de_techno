import pygame
import pygame.freetype
from enum import Enum
import os
import sys
from utils.load import *
from bucket import *
from cursor import *
from pygame.locals import *

BLUE = (106, 159, 181)
WHITE = (255, 255, 255)
WIDTH = 800
HEIGHT = 600

class UIElement(pygame.sprite.Sprite):
    """ An user interface element that can be added to a surface """

    def __init__(self, center_position, text, font_size, bg_rgb, text_rgb, action=None):
        """
        Args:
            center_position - tuple (x, y)
            text - string of text to write
            font_size - int
            bg_rgb (background colour) - tuple (r, g, b)
            text_rgb (text colour) - tuple (r, g, b)
            action - the gamestate change associated with this button
        """
        self.mouse_over = False

        default_image = create_surface_with_text(
            text=text, font_size=font_size, text_rgb=text_rgb, bg_rgb=bg_rgb
        )

        highlighted_image = create_surface_with_text(
            text=text, font_size=font_size * 1.2, text_rgb=text_rgb, bg_rgb=bg_rgb
        )

        self.images = [default_image, highlighted_image]

        self.rects = [
            default_image.get_rect(center=center_position),
            highlighted_image.get_rect(center=center_position),
        ]

        self.action = action

        super().__init__()

    @property
    def image(self):
        return self.images[1] if self.mouse_over else self.images[0]

    @property
    def rect(self):
        return self.rects[1] if self.mouse_over else self.rects[0]

    def update(self, mouse_pos, mouse_up):
        """ Updates the mouse_over variable and returns the button's
            action value when clicked.
        """
        if self.rect.collidepoint(mouse_pos):
            self.mouse_over = True
            if mouse_up:
                return self.action
        else:
            self.mouse_over = False

    def draw(self, surface):
        """ Draws element onto a surface """
        surface.blit(self.image, self.rect)

class GameState(Enum):
    QUIT = -1
    TITLE = 0
    BUCKET = 1

def main():
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    game_state = GameState.TITLE

    while True:
        if game_state == GameState.TITLE:
            game_state = title_screen(screen)

        if game_state == GameState.BUCKET:
            game_state = play_level(screen)

        if game_state == GameState.QUIT:
            pygame.quit()
            return

def create_surface_with_text(text, font_size, text_rgb, bg_rgb):
    """ Returns surface with text written on """
    font = pygame.freetype.SysFont("Courier", font_size, bold=True)
    surface, _ = font.render(text=text, fgcolor=text_rgb, bgcolor=bg_rgb)
    return surface.convert_alpha()

def title_screen(screen):
    start_btn = UIElement(
        center_position=(400, 400),
        font_size=30,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text="Start",
        action=GameState.BUCKET,
    )
    quit_btn = UIElement(
        center_position=(400, 500),
        font_size=30,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text="Quit",
        action=GameState.QUIT,
    )

    buttons = pygame.sprite.RenderUpdates(start_btn, quit_btn)

    return menu_loop(screen, buttons)


def play_level(screen):
    return_btn = UIElement(
        center_position=(140, 570),
        font_size=20,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text="Return to main menu",
        action=GameState.TITLE,
    )

    buttons = pygame.sprite.RenderUpdates(return_btn)

    return bucket_loop(screen, buttons)


def menu_loop(screen, buttons):
    """ Handles game loop until an action is return by a button in the
        buttons sprite renderer.
    """
    clock = pygame.time.Clock()

    while True:
        clock.tick(15)
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True

        screen.fill(BLUE)

        for button in buttons:
            ui_action = button.update(pygame.mouse.get_pos(), mouse_up)
            if ui_action is not None:
                return ui_action

        buttons.draw(screen)
        pygame.display.flip()

def bucket_loop(screen, buttons):
    """ Handles game loop until an action is return by a button in the
        buttons sprite renderer.
    """
    groupe = pygame.sprite.Group()

    x = 0
    y = 0
    scale = WIDTH / 3

    for i in range(3):
        bucket = Bucket(x, y, scale, 5, 3)
        groupe.add(bucket)
        x += scale

    cursor = Cursor()
    groupe.add(cursor)

    clock = pygame.time.Clock()

    objetSvg = None

    running = True

    while running:
        clock.tick(60)
        mouse_up = False
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False
            elif event.type == MOUSEBUTTONDOWN:
                for s in groupe:
                    if isinstance(s,Cursor):
                        continue
                    elif cursor.fillCursorBucket(s):
                        cursor.quantity = cursor.quantity + s.quantity
                        s.quantity = 0
                        cursor.selected = True
                        s.selected = True
                        s.printQuantity()
                        cursor.printQuantity()
                        objetSvg = s
                        break
                    elif cursor.emptyCursorBucket(s):
                        dif = s.size - s.quantity
                        if(dif >= cursor.quantity):
                            s.quantity = s.quantity + cursor.quantity
                            objetSvg.selected = False
                            objetSvg.printQuantity()
                            cursor.quantity = 0
                        else:
                            s.quantity = s.quantity + dif
                            objetSvg.selected = False
                            objetSvg.quantity = cursor.quantity - dif
                            objetSvg.printQuantity()
                            cursor.quantity = 0

                        cursor.selected = False
                        s.printQuantity()
                        cursor.printQuantity()
                        break

        """for button in buttons:
            ui_action = button.update(pygame.mouse.get_pos(), mouse_up)
            if ui_action is not None:
                return ui_action"""

    groupe.update()
    #screen.blit(BLUE)
    #buttons.draw(screen)
    groupe.draw(screen)
    pygame.display.flip()

if __name__ == "__main__":
    main()