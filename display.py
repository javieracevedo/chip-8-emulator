import pygame
import instructions
import events
from pygame.locals import *


ON = pygame.Color(255, 255, 255);
OFF = pygame.Color(0, 0, 0);

def scaled_draw(x, y, new_pixel_state, surface):
    x = x * 10
    y = y * 10



    if (new_pixel_state == ON):
        new_pixel_state = True
    else:
        new_pixel_state = False

    
    current_pixel_state = -1
    for pos_x in range(x, x+10):
        for pos_y in range(y, y+10):
            if (surface.get_at((pos_x % 640, pos_y % 320)) == ON):
                current_pixel_state = True
            else:
                current_pixel_state = False
           
            pixel = current_pixel_state != new_pixel_state
            if (pixel):
                surface.set_at((pos_x, pos_y), ON)
            else:
                surface.set_at((pos_x, pos_y), OFF)
    
