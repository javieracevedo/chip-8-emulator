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
import stack



def run():
    running = True
 
    pygame.init()
    pygame.display.set_caption("Chip-8")
    surface = pygame.display.set_mode((640, 320))
    clock = pygame.time.Clock()
    
    pygame.event.clear()
    while running:
        pygame.display.flip()
        instructions.cycle(surface)
        clock.tick(60)


memory.init()

data.load_font(memory)
memory.load_rom("roms/bc_test.ch8")
#stack.stack.append(0x03)

run()



# 16k
# 