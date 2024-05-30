import pygame
import instructions


def scaled_draw(x, y, surface):
    x = x * 10
    y = y * 10

    for pos_x in range(x, x+10):
        for pos_y in range(y, y+10):
            surface.set_at((pos_x, pos_y), pygame.Color(255, 255, 255))


def run_display():
    running = True
    
    pygame.init()
    pygame.display.set_caption("Chip-8 Screen")
    surface = pygame.display.set_mode((640, 320))
    

    instructions.CLS(surface)

    while running:
        scaled_draw(40, 31, surface)
        scaled_draw(10, 3, surface)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


