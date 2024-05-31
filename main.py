import memory
import display
import data
import instructions
import pygame



# Test Data

test_instructions = [
    "00E0",
    "6002",
    "6107",
    "6201",
    "F229",
    "D015",
    "6303",
    "6409",
    "F529",
    "D345",
    "F00A"
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


memory.init()

data.load_font(memory)

run()



