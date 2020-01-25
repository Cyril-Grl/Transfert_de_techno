import json

import pygame
from bucketGame.bucket import *
from bucketGame.cursor import *
from pygame.locals import *
from utils.enum import *
from utils.load import *
from src.csp import modelize_seaux

BLUE = (106, 159, 181)
WHITE = (255, 255, 255)


def gameBucket(screen):
    with open("seaux1.json", "r") as read:
        data = json.load(read)

    nbSeaux = data['nb seaux']
    initial = data['initial']
    final = data['final']
    contenanceMax = data['contenance max']
    solution = data['solution']

    screen_width = 800
    screen_height = 600

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Bucket Game')
    pygame.mouse.set_visible(0)
    screen.fill(BLUE)

    groupe = pygame.sprite.Group()

    x = 0
    y = 0

    height = screen_height / 3
    width = screen_width / 3

    for i in range(nbSeaux):
        bucket = Bucket(x=x, y=y, width=width, height=height, s=contenanceMax[i], q=initial[i])
        groupe.add(bucket)
        x += width
        if i == 2:
            x = 0
            y = height

    cursor = Cursor()
    groupe.add(cursor)

    clock = pygame.time.Clock()

    objetSvg = None

    font = pygame.font.Font(None, 60)
    text = font.render("Press i key ton get the help !", 1, (10, 10, 10))
    textpos = (200, 500)

    running = True

    a = 1

    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == QUIT:
                return GameState.TITLE
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return GameState.TITLE
            elif event.type == KEYDOWN and event.key == 114:
                return GameState.BUCKET
            elif event.type == KEYDOWN and event.key == 105:
                actuel = []
                for i, b in enumerate(groupe):
                    if i != len(groupe) - 1:
                        actuel.append(b._quantity)
                soluce = modelize_seaux(nb_seaux=data['nb seaux'], max_etapes=10, contenance_max=contenanceMax,
                                        contenu=actuel, fin=final)
                if len(soluce) == 0:
                    font = pygame.font.Font(None, 30)
                    text = font.render("Be sure that your bucket is empty before asking for advice!", 1, (10, 10, 10))
                else:
                    sol = soluce['etat']
                    dif1, dif2 = -1, -1
                    for i in range(len(sol[0])):
                        if sol[0][i] != sol[1][i]:
                            if dif1 == -1:
                                dif1 = i
                            else:
                                dif2 = i
                    if sol[0][dif1] > sol[1][dif1]:
                        font = pygame.font.Font(None, 30)
                        text = font.render(f'Why dont you fill the bucket {dif2 + 1} with the bucket {dif1 + 1}?', 1,
                                           (10, 10, 10))
                    else:
                        font = pygame.font.Font(None, 30)
                        text = font.render(f'Why dont you fill the bucket {dif1 + 1} with the bucket {dif2 + 1}?', 1,
                                           (10, 10, 10))
            elif event.type == MOUSEBUTTONDOWN:
                for s in groupe:
                    if isinstance(s, Cursor):
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
                        if (dif >= cursor.quantity):
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
            if isinstance(s, Cursor):
                continue

            etat.append(s.quantity)

        if etat in solution:
            a = solution.index(etat)

        if etat == final:
            return GameState.WIN

        groupe.update()
        screen.fill(BLUE)
        screen.blit(text, textpos)
        groupe.draw(screen)
        pygame.display.flip()

    return GameState.TITLE


"""
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
"""
