import pygame
import instructions
import events
from pygame.locals import *


def scaled_draw(x, y, surface):
    x = x * 10
    y = y * 10

    for pos_x in range(x, x+10):
        for pos_y in range(y, y+10):
            surface.set_at((pos_x, pos_y), pygame.Color(255, 255, 255))

