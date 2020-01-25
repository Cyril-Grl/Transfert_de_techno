import os
import sys

import pygame.freetype

sys.path.insert(1, os.path.abspath("."))

from src.utils.enum import *
from src.utils.load import *
from src.bucketGame.bucketGame import *
from src.lionGame.lionGame import *
from src.sheepGame.sheepGame import *

BLUE = (106, 159, 181)
WHITE = (255, 255, 255)

WIDTH = 800
HEIGHT = 800


class UIElement(pygame.sprite.Sprite):

    def __init__(self, center_position, text, font_size, bg_rgb, text_rgb, action=None):

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
        if self.rect.collidepoint(mouse_pos):
            self.mouse_over = True
            if mouse_up:
                return self.action
        else:
            self.mouse_over = False

    def draw(self, surface):
        surface.blit(self.image, self.rect)


def create_surface_with_text(text, font_size, text_rgb, bg_rgb):
    font = pygame.freetype.SysFont("Courier", font_size, bold=True)
    surface, _ = font.render(text=text, fgcolor=text_rgb, bgcolor=bg_rgb)
    return surface.convert_alpha()


def title_screen(screen):
    start_bucket = UIElement(
        center_position=(400, 300),
        font_size=30,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text="Start Bucket Game",
        action=GameState.BUCKET,
    )

    start_lion = UIElement(
        center_position=(400, 400),
        font_size=30,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text="Start Lion Game",
        action=GameState.LION,
    )

    start_sheep = UIElement(
        center_position=(400, 500),
        font_size=30,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text="Start Sheep Game",
        action=GameState.SHEEP,
    )

    quit_btn = UIElement(
        center_position=(400, 600),
        font_size=30,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text="Quit",
        action=GameState.QUIT,
    )

    buttons = [start_bucket, start_lion, start_sheep, quit_btn]
    clickables = pygame.sprite.RenderUpdates(buttons)

    clock = pygame.time.Clock()

    while True:
        clock.tick(15)

        mouse_up = False

        for event in pygame.event.get():
            if event.type == QUIT:
                return GameState.QUIT
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True

        screen.fill(BLUE)

        for button in buttons:
            ui_action = button.update(pygame.mouse.get_pos(), mouse_up)

            if ui_action is not None:
                return ui_action

        clickables.draw(screen)
        pygame.display.flip()


def win_screen(screen):
    image = load_image('youwin.jpg')
    sound = load_sound('winning.wav')
    sound.play()
    clock = pygame.time.Clock()

    while True:
        clock.tick(15)

        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                return GameState.TITLE

        screen.fill(BLUE)
        screen.blit(image, (150, 150))
        pygame.display.flip()


def lose_screen(screen):
    image = load_image('youlose.jpg')
    sound = load_sound('loosing.wav')
    sound.play()
    clock = pygame.time.Clock()

    while True:
        clock.tick(15)

        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                return GameState.TITLE

        screen.fill(BLUE)
        screen.blit(image, (150, 150))
        pygame.display.flip()


def main():
    pygame.init()
    pygame.mixer.pre_init(44100, 16, 2, 4096)

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Minizinc Fever')

    game_state = GameState.TITLE

    clock = pygame.time.Clock()

    while True:
        clock.tick(15)

        if game_state == GameState.TITLE:
            game_state = title_screen(screen)

        if game_state == GameState.BUCKET:
            game_state = gameBucket(screen)
            screen = pygame.display.set_mode((WIDTH, HEIGHT))
            pygame.mouse.set_visible(1)

        if game_state == GameState.LION:
            game_state = gameLion(screen)
            screen = pygame.display.set_mode((WIDTH, HEIGHT))
            pygame.mouse.set_visible(1)

        if game_state == GameState.SHEEP:
            game_state = gameSheep(screen)
            screen = pygame.display.set_mode((WIDTH, HEIGHT))
            pygame.mouse.set_visible(1)

        if game_state == GameState.WIN:
            game_state = win_screen(screen)

        if game_state == GameState.LOSE:
            game_state = lose_screen(screen)

        if game_state == GameState.QUIT:
            pygame.quit()
            return


if __name__ == "__main__":
    main()
