import os
import sys
import pygame

from pygame.locals import *
from sheepGame.sheep import *
from utils.enum import *

BLUE = (106, 159, 181)

WIDTH = 1200
HEIGHT = 200

def gameSheep(screen):
    nb_beasts = 4

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Sheep Game')

    picture_width = WIDTH / (nb_beasts + 1)
    x = 0
    position = 1

    l = []

    for i in range(int(nb_beasts / 2)):
        sheep = Sheep(x = x, y = 0, width = picture_width, height = HEIGHT, sheep = True, position = position, screenWidth = WIDTH)
        l.append(sheep)
        x += picture_width
        position += 1

    x = WIDTH - picture_width
    position = nb_beasts + 1

    for i in range(int(nb_beasts / 2)):
        sheepBlack = Sheep(x = x, y = 0, width = picture_width, height = HEIGHT, sheep = False, position = position, screenWidth = WIDTH)
        l.append(sheepBlack)
        x -= picture_width
        position -= 1

    clickables = pygame.sprite.RenderUpdates(l)

    clock = pygame.time.Clock()

    running = True

    # main loop
    while running:

        clock.tick(60)

        mouse_up_right = False
        mouse_up_left = False

        for event in pygame.event.get():
            if event.type == QUIT:
                return GameState.TITLE
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return GameState.TITLE
            elif event.type == KEYDOWN and event.key == 114:
                return GameState.SHEEP
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            	mouse_up_left = True
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                mouse_up_right = True
        
        screen.fill(BLUE)

        for clickable in clickables:
            if clickable.update(mouse_pos = pygame.mouse.get_pos(), mouse_up_right = mouse_up_right, mouse_up_left = mouse_up_left):
                clickable.moveBeast(etat = l)

        clickables.draw(screen)
        pygame.display.flip()