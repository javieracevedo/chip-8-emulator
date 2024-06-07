import memory
import display
import data
import instructions
import pygame
import time
import registers
import data
import struct
import numpy as np
import debug
import sys
import os
from pygame.locals import *



# Test Data
test_instructions = [
    #"00E0", # Clear the Screen
    # Drawn A Sprite
    "6400", # Set X co-ordinate
    "6500", # Set Y co-ordinate
    "620A", # Put the number A in V2
    "F229", # Point to the A font
    "D455", # Draw Sprite

    # Draw B Sprite
    "6406",
    "6500",
    "620B",
    "F229",
    "D455",

    # Draw C Sprite
    "640C",
    "6500",
    "620C",
    "F229",
    "D455",

    # Draw D Sprite
    "6412",
    "6500",
    "620D",
    "F229",
    "D455",

    # Draw E Sprite
    "6418",
    "6500",
    "620E",
    "F229",
    "D455",

    # Draw F Sprite
    "641E",
    "6500",
    "620F",
    "F229",
    "D455",

    # Draw 1 Sprite
    "6424",
    "6500",
    "6201",
    "F229",
    "D455",

    # Draw 2 Sprite
    "642A",
    "6500",
    "6202",
    "F229",
    "D455",
    
    # Draw 3 Sprite
    "6430",
    "6500",
    "6203",
    "F229",
    "D455",

    # Draw 4 Sprite
    "6436",
    "6500",
    "6204",
    "F229",
    "D455",

    # Draw 5 Sprite
    "6400",
    "6506",
    "6205",
    "F229",
    "D455",
    
    # Draw 6 Sprite
    "6406",
    "6506",
    "6206",
    "F229",
    "D455",

    # Draw 7 Sprite
    "640C",
    "6506",
    "6207",
    "F229",
    "D455",

    # Draw 8 Sprite
    "6412",
    "6506",
    "6208",
    "F229",
    "D455",

    # Draw 9 Sprite
    "6418",
    "6506",
    "6209",
    "F229",
    "D455",

    # Draw a random sprite
    "641B",
    "651B",
    "F229",
    "A200",
    "D455",
]


ibm_instructions = []


def run():
    running = True
 
    pygame.init()
    pygame.display.set_caption("Chip-8")
    surface = pygame.display.set_mode((640, 320))
    
    pygame.event.clear()
    while running:
        pygame.display.flip()

        instructions.execute_instructions(ibm_instructions, surface)
        time.sleep(1./25)
        


with open("roms/ibm.ch8", mode='rb') as file:
    lines = file.readlines()
    lines = np.array(lines).flatten()[0]
    
    for idx in range(0, len(lines), 2):
        first = struct.unpack(">ss", lines[idx:idx+2])[0].hex()
        second = struct.unpack(">ss", lines[idx:idx+2])[1].hex()
        merged = str(first) + str(second)
        ibm_instructions.append(merged.upper())


memory.init()

data.load_sprites(memory)
data.load_font(memory)

run()

