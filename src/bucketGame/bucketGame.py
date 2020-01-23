import os
import sys
import pygame
import json

sys.path.insert(1, os.path.abspath("."))

from utils.load import *
from bucket import *
from cursor import *
from pygame.locals import *

with open("seaux1.json", "r") as read:
    data = json.load(read)

nbSeaux = data['nb seaux']
initial = data['initial']
final = data['final']
contenanceMax = data['contenance max']
solution = data['solution']

print(data)

screen_width = 800
screen_height = 600

# Init pygame
pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init()

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Minizinc Fever')
pygame.mouse.set_visible(0)

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((250, 250, 250))

screen.blit(background, (0, 0))
pygame.display.flip()

groupe = pygame.sprite.Group()

x = 0
y = 0
height = screen_height / 3
width = screen_width / 3

for i in range(nbSeaux):
  bucket = Bucket(x = x, y = y, width = width, height = height, s = contenanceMax[i], q = initial[i])
  groupe.add(bucket)
  x += width
  if i == 2:
    x = 0
    y = height

cursor = Cursor()
groupe.add(cursor)

clock = pygame.time.Clock()

objetSvg = None

font = pygame.font.Font(None,60)
text = font.render("Press i key ton get the help !",1,(10, 10, 10))
textpos = (200,500)

running = True

a = 1

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            running = False
        elif event.type == KEYDOWN and event.key == 105:
            font = pygame.font.Font(None, 30)
            text = font.render(str(solution[a + 1]),1,(10, 10, 10))
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

    etat = []
    for s in groupe:
        if isinstance(s,Cursor):
            continue
        
        etat.append(s.quantity)

    if etat in solution:
        a = solution.index(etat)

    if etat == final:
        running = False

    groupe.update()
    screen.blit(background, (0, 0))
    screen.blit(text, textpos)
    groupe.draw(screen)
    pygame.display.flip()

image = load_image('youwin.jpg', -1)
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            running = False
    
    screen.blit(background, (0, 0))   
    screen.blit(image, (0,0))
    pygame.display.flip()

pygame.display.quit()