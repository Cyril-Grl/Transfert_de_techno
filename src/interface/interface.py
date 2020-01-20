import os
import sys
import pygame
from utils.load import *
from bucket import *
from cursor import *
from pygame.locals import *

screen_width = 1280
screen_height = 720

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
y = screen_height / 2
scale = screen_width / 3

for i in range(3):
  bucket = Bucket(x, y, scale, 5, 3)
  groupe.add(bucket)
  x += scale

cursor = Cursor()
groupe.add(cursor)

clock = pygame.time.Clock()

LEFT = 1
RIGHT = 3

objetSvg = None

running = True

while running:
    clock.tick(60)

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

    groupe.update()
    screen.blit(background, (0, 0))
    groupe.draw(screen)
    pygame.display.flip()

pygame.display.quit()
"""
screen_width = 1280
screen_height = 720

pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Monkey Fever')
pygame.mouse.set_visible(0)

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((250, 250, 250))

if pygame.font:
    font = pygame.font.Font(None, 36)
    text = font.render("Pummel The Chimp, And Win $$$", 1, (10, 10, 10))
    textpos = text.get_rect(centerx=background.get_width()/2)
    background.blit(text, textpos)

screen.blit(background, (0, 0))
pygame.display.flip()

whiff_sound = load_sound('Chirping-Birds.wav')
punch_sound = load_sound('Chirping-Birds.wav')
chimp = Chimp()
fist = Fist()
allsprites = pygame.sprite.RenderPlain((fist, chimp))
clock = pygame.time.Clock()

while 1:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            if fist.punch(chimp):
                punch_sound.play() #frappé
                chimp.punched()
            else:
                whiff_sound.play() #raté
        elif event.type == MOUSEBUTTONUP:
            fist.unpunch()
    allsprites.update()
    screen.blit(background, (0, 0))
    allsprites.draw(screen)
    pygame.display.flip()
"""