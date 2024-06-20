import pygame
from pygame.locals import *


# Supported Key Codes

key_codes = {
    "48": 0x0,
    "49": 0x1,
    "50": 0x2,
    "51": 0x3,
    "52": 0x4,
    "53": 0x5,
    "54": 0x6,
    "55": 0x7,
    "56": 0x8,
    "57": 0x9,
    "97": 0xA,
    "98": 0xB,
    "99": 0xC,
    "100": 0xD,
    "101": 0xE,
    "102": 0xF
}


def wait_for_keypress():
    while True:
        event = pygame.event.wait()

        if (event.type == pygame.QUIT):
            pygame.quit()
        elif (event.type == pygame.KEYDOWN):
            if str(event.key) in key_codes:
                return key_codes[str(event.key)]

