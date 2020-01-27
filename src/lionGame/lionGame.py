import json

from pygame.locals import *

from lionGame.buffalo import *
from lionGame.lion import *
from utils.enum import *
from csp import modelize_riviere1

BLUE = (106, 159, 181)

WIDTH = 800
HEIGHT = 1000

GAME_HEIGHT = 800


def gameLion(screen, path):
    with open(path, "r") as read:
        data = json.load(read)

    nb_bison = data["nb bisons"]
    solution = data["solution"]
    transferts = data["transferts"]
    final = solution[data["nb etapes"] - 1]

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Lion Game')

    split_width = WIDTH / 3
    split_height = GAME_HEIGHT / (nb_bison * 2)

    y = 0

    l = []

    for i in range(nb_bison):
        buffalo = Buffalo(x=0, y=y, width=split_width, height=split_height)
        l.append(buffalo)
        y += split_height

    for i in range(nb_bison):
        lion = Lion(x=0, y=y, width=split_width, height=split_height)
        l.append(lion)
        y += split_height

    clickables = pygame.sprite.RenderUpdates(l)

    font = pygame.font.Font(None, 30)

    text = font.render("Press i key ton get the help !", 1, (10, 10, 10))
    textpos = (0, 900)

    text_switch = font.render("Press v to switch side the boat !", 1, (10, 10, 10))
    text_switchpos = (400, 900)

    boat_right = False

    clock = pygame.time.Clock()
    running = True

    # main loop
    while running:
        clock.tick(60)

        mouse_up_right = False
        mouse_up_left = False
        is_boat_full = False
        nb_beast_on_boat = 0
        etat = []

        for beast in clickables:
            etat.append(beast.position)
            if beast.position == 3:
                nb_beast_on_boat += 1

        if etat in solution:
            a = solution.index(etat)

        if etat == final:
            return GameState.WIN

        if nb_beast_on_boat == 2:
            is_boat_full = True

        for event in pygame.event.get():
            if event.type == QUIT:
                return GameState.TITLE
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return GameState.TITLE
            elif event.type == KEYDOWN and event.key == 114:
                return GameState.LION
            elif event.type == KEYDOWN and event.key == 118 and nb_beast_on_boat >= 1:
                text = font.render("Press i for advice!", 1, (10, 10, 10))
                if boat_right:
                    boat_right = False
                    text_switch = font.render("Boat Left !", 1, (10, 10, 10))
                else:
                    boat_right = True
                    text_switch = font.render("Boat Right !", 1, (10, 10, 10))

                nb_lion_right = 0
                nb_lion_left = 0
                nb_buffalo_right = 0
                nb_buffalo_left = 0

                for i in range(nb_bison):
                    if l[i].position == 1:
                        nb_buffalo_left += 1
                    elif l[i].position == 2:
                        nb_buffalo_right += 1

                for i in range(nb_bison, nb_bison * 2):
                    if l[i].position == 1:
                        nb_lion_left += 1
                    elif l[i].position == 2:
                        nb_lion_right += 1

                if nb_lion_right > nb_buffalo_right != 0:
                    return GameState.LOSE

                if nb_lion_left > nb_buffalo_left != 0:
                    return GameState.LOSE

            elif event.type == KEYDOWN and event.key == 105:
                if any(e == 3 for e in etat):
                    text = font.render("The boat must be empty!", 1, (10, 10, 10))
                else:
                    soluce = modelize_riviere1(nb_bison=int(len(etat)/2), max_etapes=10, init=etat, radeau=boat_right)
                    if len(soluce) == 0:
                        font = pygame.font.Font(None, 30)
                        text = font.render("I dont want to help you!", 1, (10, 10, 10))
                    else:
                        sol = soluce['transfered']
                        to_transfer = []
                        for i in sol[1]:
                            if i <= int(len(etat)/2):
                                to_transfer.append('Bison ')
                            else:
                                to_transfer.append('Lion ')
                        text = font.render("Move : "+"".join(to_transfer), 1, (10, 10, 10))
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up_left = True
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                mouse_up_right = True

        screen.fill(BLUE)

        for clickable in clickables:
            if clickable.update(mouse_pos=pygame.mouse.get_pos(), mouse_up_right=mouse_up_right,
                                mouse_up_left=mouse_up_left):
                clickable.moveBeast(boatRight=boat_right, isBoatFull=is_boat_full)

        screen.blit(text_switch, text_switchpos)
        screen.blit(text, textpos)
        clickables.draw(screen)
        pygame.display.flip()
