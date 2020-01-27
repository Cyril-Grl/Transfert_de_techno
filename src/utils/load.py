import os
import sys

import pygame
from pygame.locals import *


def load_image(name, colorkey=None):
    fullname = os.path.join(os.path.abspath("."), "data/" + name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print("Impossible de charger l'image : " + fullname)
        sys.exit(message)
    image = image.convert()
    if colorkey != None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image


def load_sound(name):
    class NoneSound:
        def play(self): pass

    if not pygame.mixer:
        return NoneSound()
    fullname = os.path.join(os.path.abspath("."), "data/" + name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error as message:
        print("Impossible de charger le son : " + fullname)
        sys.exit(message)
    return sound
