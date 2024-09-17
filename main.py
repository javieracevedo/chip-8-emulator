import pygame
import time
import struct
import sys
import os
from pygame.locals import *
import numpy as np
import random


config_sprite_color = 0xFFFFFF
config_bg_color = 0x000000
config_rom_path = ""

MEM_SIZE_KB = 4096
CLOCK_SPEED_HZ = 640
CYCLE_DELAY = 1.0 / CLOCK_SPEED_HZ

memory = [0] * MEM_SIZE_KB
V = [0] * 16
I = 0
stack = [0]
pc = 0x200
delay_timer = 0
sound_timer = 0

font_list = [
    [0xF0, 0x90, 0x90, 0x90, 0xF0],
    [0x20, 0x60, 0x20, 0x20, 0x70],
    [0xF0, 0x10, 0xF0, 0x80, 0xF0],
    [0xF0, 0x10, 0xF0, 0x10, 0xF0],
    [0x90, 0x90, 0xF0, 0x10, 0x10],
    [0xF0, 0x80, 0xF0, 0x10, 0xF0],
    [0xF0, 0x80, 0xF0, 0x90, 0xF0],
    [0xF0, 0x10, 0x20, 0x40, 0x40],
    [0xF0, 0x90, 0xF0, 0x90, 0xF0],
    [0xF0, 0x90, 0xF0, 0x10, 0xF0],
    [0xF0, 0x90, 0xF0, 0x90, 0x90],
    [0xE0, 0x90, 0xE0, 0x90, 0xE0],
    [0xF0, 0x80, 0x80, 0x80, 0xF0],
    [0xE0, 0x90, 0x90, 0x90, 0xE0],
    [0xF0, 0x80, 0xF0, 0x80, 0xF0],
    [0xF0, 0x80, 0xF0, 0x80, 0x80]
]

supported_keycodes = {
    "49": 0x1,
    "50": 0x2,
    "51": 0x3,
    "52": 0xC,
    "113": 0x4,
    "119": 0x5,
    "101": 0x6,
    "114": 0xD,
    "97": 0x7,
    "115": 0x8,
    "100": 0x9,
    "102": 0xE,
    "122": 0xA,
    "120": 0x0,
    "99": 0xB,
    "118": 0xF
}
inverted_keycodes = {v: int(k) for k, v in supported_keycodes.items()}


def scaled_draw(x, y, new_pixel_state, surface):
    global V
    global config_sprite_color, config_bg_color
    x = x * 10
    y = y * 10

    new_pixel_state = True if new_pixel_state == pygame.Color(config_sprite_color) else False
    current_pixel_state = True if surface.get_at((x, y % 320)) == pygame.Color(config_sprite_color) else  False
    pixel = current_pixel_state != new_pixel_state

    if (pixel):
        pygame.draw.rect(surface, config_sprite_color, [x, y, 10, 10]) 
    else:
        pygame.draw.rect(surface, config_bg_color, [x, y, 10, 10])
        if (current_pixel_state and new_pixel_state):
            surface.set_at((x, y), config_bg_color)
            V[0xF] = 1

def load_rom(file_path):
    global memory
    with open(file_path, mode='rb') as file:
        rom_data = file.read()

    for idx in range(len(rom_data)):
        byte = struct.unpack("B", rom_data[idx:idx + 1])[0]
        memory[idx + 0x200] = byte

def load_font(memory):
    flattened_font = [byte for char in font_list for byte in char]
    for i in range(len(flattened_font)):
        if 0x50 + i < MEM_SIZE_KB:
            memory[0x50 + i] = flattened_font[i]
        else:
            print(f"Warning: Attempt to write out of memory bounds at address {0x50 + i}")

def wait_for_keypress():
    global delay_timer
    pygame.event.clear()

    while True:
        if delay_timer > 0:
            delay_timer -= 1

        event = pygame.event.wait()

        if (event.type == pygame.QUIT):
            pygame.quit()
        elif (event.type == pygame.KEYUP):
            if str(event.key) in supported_keycodes:
                return supported_keycodes[str(event.key)]

def execute_instruction(instruction, surface):
    global V, stack, pc, I, memory, delay_timer, sound_timer
    global config_bg_color

    lhs_subcode = instruction >> 12 & 0x000F
    rhs_subcode = instruction & 0x000F
    vx = instruction >> 8 & 0x000F
    vy = instruction >> 4 & 0x000F
    n = instruction & 0x000f
    nn = instruction & 0x00FF; kk = nn
    nnn = instruction & 0x0FFF

    if instruction == 0x00E0:
        surface.fill(config_bg_color)
        pygame.display.flip()
    elif instruction == 0x00EE:
        pc = stack.pop()
    elif lhs_subcode == 0x6:
        V[vx] = kk
    elif lhs_subcode == 0x7:
        V[vx] = (V[vx] + nn) % 256
    elif lhs_subcode == 0x0F:
        if nn == 0x29:
            vx_addr = 0x50 + (V[vx] * 5)
            if (vx_addr): I = vx_addr
        elif nn == 0x55:
            for n in range(vx + 1): memory[I + n] = V[n]
            I += 1
        elif nn == 0x65:
            for n in range(vx + 1): V[n] = memory[I + n]
            I += 1
        elif nn == 0x33:
            value = V[vx]
            memory[I + 2] = value % 10
            value //= 10
            memory[I + 1] = value % 10
            value //= 10
            memory[I] = value % 10
        elif nn == 0x1E:
            I = (V[vx] + I) % 0x1000
        elif nn == 0x15:
            delay_timer = V[vx]
        elif nn == 0x07:
            V[vx] = delay_timer
        elif nn == 0xA:
            key = wait_for_keypress()
            V[vx] = key
        elif nn == 0x18:
            sound_timer = V[vx]
    elif lhs_subcode == 0xD:
        mem_slice = memory[I:I+n]
        pos_x = V[vx] % 64
        pos_y = V[vy] % 32

        V[0xF] = 0

        binaries = [format(integer, '08b') for integer in mem_slice]
        for binary in binaries:
            for idx in range(8):
                pixel_state = pygame.Color(config_sprite_color) if binary[idx] == '1' else config_bg_color               
                # If you start drawing before the limit (width) then draw what you can draw, but
                # once you pass the limit, stop
                if (pos_y > 31 or pos_x + idx > 63):
                    break
                scaled_draw(pos_x + idx, pos_y, pixel_state, surface)
            pos_y += 1

        pygame.display.flip()
    elif lhs_subcode == 0x1:
        pc = nnn
    elif lhs_subcode == 0xB:
        pc = nnn
    elif lhs_subcode == 0xC:
        V[vx] = random.randint(0, 255) & nn
    elif lhs_subcode == 0xA:
        I = nnn
    elif lhs_subcode == 0x2:
        stack.append(pc)
        pc = nnn
    elif lhs_subcode == 0x3:
        if (V[vx] == nn):
            pc += 0x2
    elif lhs_subcode == 0x5:
        if (V[vx] == V[vy]):
            pc += 0x2
    elif lhs_subcode == 0x4:
        if V[vx] != nn:
            pc += 0x2
    elif lhs_subcode == 0x8:
        subcode = rhs_subcode
        if (subcode == 0x0):
            V[vx] = V[vy]
        if subcode == 0x5:
            old_vx = V[vx]
            old_vy = V[vy]
            V[vx] = (V[vx] - V[vy]) % 256
            V[0xF] = 1
            if old_vx < old_vy:
                V[0xF] = 0
        elif subcode == 0x7:
            old_vx = V[vx]
            old_vy = V[vy]
            V[vx] = (V[vy] - V[vx]) % 256
            V[0xF] = 1
            if old_vy < old_vx:
                V[0xF] = 0
        elif subcode == 0x1:
            V[vx] |= V[vy]
            V[0xF] = 0
        elif subcode == 0x2:
            V[vx] &= V[vy]
            V[0xF] = 0
        elif subcode == 0x4:
            result = V[vx] + V[vy]
            V[vx] = (V[vx] + V[vy]) % 256
            if (result > 255):
                V[0xF] = 1
            else:
                V[0xF] = 0
        elif subcode == 0x3:
            V[vx] ^= V[vy]
            V[0xF] = 0
        elif subcode == 0xE:
            V[vx] = V[vy]
            old_vx = V[vx]
            V[vx] = (V[vx] << 1) % 256
            V[0xF] = (old_vx >> 7) & 1
        elif subcode == 0x6:
            V[vx] = V[vy]
            old_vx  = V[vx]
            V[vx] >>= 1
            V[0xF] = old_vx & 1
    elif lhs_subcode == 0x9:
        if V[vx] != V[vy]: pc += 0x2
    elif lhs_subcode == 0xE:
        key_codes = list(map(lambda e: e.key if e.type == pygame.KEYDOWN else None, pygame.event.get()))
        if (nn == 0xA1):
            if (inverted_keycodes[V[vx]] not in key_codes):
                pc += 0x2
        elif (nn == 0x9E):
            if (inverted_keycodes[V[vx]] in key_codes):
                pc += 0x2

def fetch():
    global pc
    instruction = memory[pc:pc+2]
    pc += 0x2
    return instruction

def decode(memory_slice):
    first_byte = hex(memory_slice[0])[2:].zfill(2)
    if (len(memory_slice) == 2):
        second_byte = hex(memory_slice[1])[2:].zfill(2)
        return int(first_byte + second_byte, 16)
    else:
        return int(first_byte, 16)

def cycle(surface):
    instruction = fetch()
    instruction = decode(instruction)
    execute_instruction(instruction, surface)

def run():
    global delay_timer, sound_timer

    running = True

    pygame.init()

    pygame.key.set_repeat(1)
    pygame.display.set_caption("Chip-8")

    surface = pygame.display.set_mode((640, 320))
    surface.fill(config_bg_color)

    pygame.event.clear()
    
    while running:
        start_time = time.time()
        elapsed_time = time.time() - start_time

        cycle(surface)

        if delay_timer > 0:
            delay_timer -= 1
        if sound_timer > 0:
            sound_timer -= 1
        
        if elapsed_time < CYCLE_DELAY:
            time.sleep(CYCLE_DELAY - elapsed_time)

def parse_arg_options(argument):
    splitted_args = argument.split("=")
    option_name = splitted_args[0]
    if (len(splitted_args) > 1):
        option_value = splitted_args[1]
        return (option_name, option_value)
    return (option_name, None)

def apply_config(parsed_options):
    global config_rom_path, config_bg_color, config_sprite_color
    for option in parsed_options:
        option_val = option[1]
        if "--color" in option:
            if (len(option_val) < 8): raise ValueError
            config_sprite_color = option_val[0:8]
        if "--bgcolor" in option:
            if (len(option_val) < 8): raise ValueError
            config_bg_color = option_val[0:8]
        if "--rom-path" in option:
            config_rom_path = option_val


parsed_options = [parse_arg_options(argument) for argument in sys.argv]
try:
    apply_config(parsed_options)
except ValueError:
    print("Error: color string should have at least 8 numbers.")
    exit()

try:
    load_rom(config_rom_path)
except FileNotFoundError:
    print("Error: could not find rom file: " + config_rom_path)
    exit()

load_font(memory)

run()
