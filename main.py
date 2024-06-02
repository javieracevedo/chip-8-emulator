import memory
import display
import data
import instructions
import pygame
import time

# Test Data

test_instructions = [
    "00E0", # Clear the Screen
   
    # Drawn A Sprite
    "6000", # Set X co-ordinate
    "6100", # Set Y co-ordinate
    "620A", # Put the number A in V2
    "F229", # Point to the A font
    "D015", # Draw Sprite

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
    "D455"
]


def run():
    running = True
    
    pygame.init()
    pygame.display.set_caption("Chip-8 Screen")
    surface = pygame.display.set_mode((640, 320))


    instructions.CLS(surface)


    pygame.event.clear()
    while running:
        pygame.display.flip()
        instructions.execute_instructions(test_instructions, surface)
        time.sleep(1./25)
memory.init()

data.load_font(memory)



run()



