import memory
import display
import data
import instructions
import pygame
import time
import registers
import data

# Test Data

test_instructions = [
    "00E0", # Clear the Screen
   
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
    "D454",


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
    "D455"
]

def run():
    running = True
    
    pygame.init()
    pygame.display.set_caption("Chip-8")
    surface = pygame.display.set_mode((640, 320))


    instructions.CLS(surface)
    

    pygame.event.clear()
    while running:
        pygame.display.flip()
    
        #Draw one of the sprites in 0x200 memory location
        registers.V[0] = '0x1B'
        registers.V[1] = '0x1B'
        registers.I = 0x200
        instructions.DRW(0, 1, 5, surface);


        instructions.execute_instructions(test_instructions, surface)
        time.sleep(1./60)



memory.init()

data.load_sprites(memory)
data.load_font(memory)

run()

