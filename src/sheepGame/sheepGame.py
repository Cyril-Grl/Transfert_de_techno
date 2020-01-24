import os
import sys
import pygame

sys.path.insert(1, os.path.abspath("."))

from pygame.locals import *
from sheep import *

BLUE = (106, 159, 181)

nbBeasts = 4

screen_width = 1200
screen_height = 200

# Init pygame
pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init()

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Minizinc Fever')

width = screen_width / (nbBeasts + 1)
x = 0
position = 1

l = []

for i in range(int(nbBeasts / 2)):
    sheep = Sheep(x = x, y = 0, width = width, height = screen_height, sheep = True, position = position, screenWidth = screen_width)
    l.append(sheep)
    x += width
    position += 1

x = screen_width - width
position = nbBeasts + 1

for i in range(int(nbBeasts / 2)):
    sheepBlack = Sheep(x = x, y = 0, width = width, height = screen_height, sheep = False, position = position, screenWidth = screen_width)
    l.append(sheepBlack)
    x -= width
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
            running = False
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            running = False
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