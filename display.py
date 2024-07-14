import pygame
import instructions
import events
from pygame.locals import *

ON = pygame.Color(255, 255, 255)
OFF = pygame.Color(0, 0, 0)

def scaled_draw(x, y, new_pixel_state, surface):
    # Scale coordinates to the display size
    x = (x * 10) % 640
    y = (y * 10) % 320

    # Determine the pixel state
    new_pixel_state = (new_pixel_state == ON)

    # Determine the current pixel state by checking the color at the center of the 10x10 block
    current_pixel_state = (surface.get_at((x, y)) == ON)

    # XOR the current pixel state with the new pixel state
    pixel = current_pixel_state != new_pixel_state

    # Determine the color to set based on the pixel state
    color = ON if pixel else OFF

    # Draw the 10x10 block
    pygame.draw.rect(surface, color, pygame.Rect(x, y, 10, 10))
