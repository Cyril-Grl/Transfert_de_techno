import os
import sys
import pygame
import json

sys.path.insert(1, os.path.abspath("."))

from pygame.locals import *
from lion import *
from buffalo import *

with open("riviere1.json", "r") as read:
    data = json.load(read)

nbBison = data["nb bisons"]
solution = data["solution"]
transferts = data["transferts"]
final = solution[data["nb etapes"] - 1]

BLUE = (106, 159, 181)

screen_width = 800
screen_height = 800

image_height = 1000

# Init pygame
pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init()

screen = pygame.display.set_mode((screen_width, image_height))
pygame.display.set_caption('Minizinc Fever')

width = screen_width / 3
height = screen_height / (nbBison * 2)

y = 0

l = []

for i in range(nbBison):
    lion = Lion(x = 0, y = y, width = width, height = height)
    l.append(lion)
    y += height

for i in range(nbBison):
    buffalo = Buffalo(x = 0, y = y, width = width, height = height)
    l.append(buffalo)
    y += height


clickables = pygame.sprite.RenderUpdates(l)

clock = pygame.time.Clock()

font = pygame.font.Font(None,30)
text = font.render("Press i key ton get the help !",1,(10, 10, 10))
textpos = (0,900)

textSwitch = font.render("Press v to switch side the boat !",1,(10, 10, 10))
textSwitchpos = (400,900)

boatRight = False

running = True

# main loop
while running:
    clock.tick(60)

    mouse_up_right = False
    mouse_up_left = False
    isBoatFull = False

    nbBeastOnBoat = 0

    etat = []
    for beast in clickables:
        etat.append(beast.position)
        if beast.position == 3:
            nbBeastOnBoat += 1

    if etat in solution:
        a = solution.index(etat)

    if etat == final:
        running = False

    if nbBeastOnBoat == 2:
        isBoatFull = True

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            running = False
        elif event.type == KEYDOWN and event.key == 118:
            if boatRight:
                boatRight = False
                textSwitch = font.render("Boat Left !",1,(10, 10, 10))
            else:
                boatRight = True
                textSwitch = font.render("Boat Right !",1,(10, 10, 10))

            nbLionRight = 0
            nbLionLeft = 0
            nbBuffaloRight = 0
            nbBuffaloLeft = 0

            for i in range(nbBison):
                if l[i].position == 1:
                    nbLionLeft += 1
                elif l[i].position == 2:
                    nbLionRight += 1

            for i in range(nbBison, nbBison * 2):
                if l[i].position == 1:
                    nbBuffaloLeft += 1
                elif l[i].position == 2:
                    nbBuffaloRight += 1

            if nbLionRight > nbBuffaloRight and nbBuffaloRight != 0:
                running = False

            if nbLionLeft > nbBuffaloLeft and nbBuffaloLeft != 0:
                running = False

        elif event.type == KEYDOWN and event.key == 105:
            text = font.render(str(solution[a + 1]),1,(10, 10, 10))
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            mouse_up_left = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 3:
            mouse_up_right = True
    
    screen.fill(BLUE)

    for clickable in clickables:
    	if clickable.update(mouse_pos = pygame.mouse.get_pos(), mouse_up_right = mouse_up_right, mouse_up_left = mouse_up_left):
    		clickable.moveBeast(boatRight = boatRight, isBoatFull = isBoatFull)

    screen.blit(textSwitch, textSwitchpos)
    screen.blit(text, textpos)
    clickables.draw(screen)
    pygame.display.flip()

pygame.display.quit()