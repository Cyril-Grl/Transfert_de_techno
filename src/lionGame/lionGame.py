import os
import sys
import pygame

sys.path.insert(1, os.path.abspath("."))

from pygame.locals import *
from lion import *
from buffalo import *

BLUE = (106, 159, 181)

screen_width = 800
screen_height = 600

# Init pygame
pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init()

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Minizinc Fever')

width = screen_width / 3
height = screen_height / 3

lion1 = Lion(x = 0, y = 0, width = width, height = height)
lion2 = Lion(x = 0, y = 0 + height, width = width, height = height)
buffalo = Buffalo(x = 0, y = height + height, width = width, height = height)

l = [lion1, lion2, buffalo]
clickables = pygame.sprite.RenderUpdates(l)

beastRight = []
beastBoat = []
beastLeft = []

lion_on_the_right = True
lion_on_the_left = False
lion_on_the_boat = False
beast_on_the_boat = False

# main loop
while True:

    mouse_up = False

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
        	mouse_up = True
    
    screen.fill(BLUE)

    for clickable in clickables:
    	if clickable.update(pygame.mouse.get_pos(), mouse_up):
    		clickable.moveBeast()

    clickables.draw(screen)
    pygame.display.flip()