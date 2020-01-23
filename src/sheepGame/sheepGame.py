import os
import sys
import pygame

sys.path.insert(1, os.path.abspath("."))

from pygame.locals import *
from sheep import *

BLUE = (106, 159, 181)

screen_width = 1200
screen_height = 200

# Init pygame
pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init()

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Minizinc Fever')

width = screen_width / 6

sheepWhite1 = Sheep(x = 0, y = 0, width = width, height = screen_height, sheep = True)
sheepWhite2 = Sheep(x = width, y = 0, width = width, height = screen_height, sheep = True)
sheepWhite3 = Sheep(x = width * 2, y = 0, width = width, height = screen_height, sheep = True)

sheepBlack1 = Sheep(x = screen_width - width, y = 0, width = width, height = screen_height, sheep = False)
sheepBlack2 = Sheep(x = screen_width - width * 2, y = 0, width = width, height = screen_height, sheep = False)

l = [sheepWhite1, sheepWhite2, sheepWhite3, sheepBlack1, sheepBlack2]
clickables = pygame.sprite.RenderUpdates(l)

# main loop
while True:

    mouse_up_right = False
    mouse_up_left = False

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
        	mouse_up_left = True
        if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
            mouse_up_right = True
    
    screen.fill(BLUE)

    for clickable in clickables:
        if clickable.update(mouse_pos = pygame.mouse.get_pos(), mouse_up_right = mouse_up_right, mouse_up_left = mouse_up_left):
            clickable.moveBeast()

    clickables.draw(screen)
    pygame.display.flip()