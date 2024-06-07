import memory
import display
import data
import instructions
import pygame
import time
import registers
import data
import struct
import sys
import os
import pc
import debug
from pygame.locals import *
import numpy as np



def run():
    running = True
 
    pygame.init()
    pygame.display.set_caption("Chip-8")
    surface = pygame.display.set_mode((640, 320))
    clock = pygame.time.Clock()
    
    pygame.event.clear()
    while running:
        pygame.display.flip()
        instruction = instructions.fetch()
        instruction = instructions.decode(instruction)
        instructions.execute_instruction(instruction.upper(), surface) 
        clock.tick(60)


memory.init()

data.load_font(memory)
memory.load_rom("roms/ibm.ch8")

run()

