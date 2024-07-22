import pygame
import time
import struct
import sys
import os
from pygame.locals import *
import numpy as np
import random


memory = [0] * 4096 # 4KB memory
V = [0] * 16
I = 0
stack = [0]
pc = 0x200
delay_timer = 0
sound_timer = 0


# *DATA*

font = {
    "0x0": [0xf0, 0x90, 0x90, 0x90, 0xf0],
    "0x1": [0x20, 0x60, 0x20, 0x20, 0x70],
    "0x2": [0xf0, 0x10, 0xf0, 0x80, 0xf0],
    "0x3": [0xf0, 0x10, 0xf0, 0x10, 0xf0],
    "0x4": [0x90, 0x90, 0xf0, 0x10, 0x10],
    "0x5": [0xf0, 0x80, 0xf0, 0x10, 0xf0],
    "0x6": [0xf0, 0x80, 0xf0, 0x90, 0xf0],
    "0x7": [0xf0, 0x10, 0x20, 0x40, 0x40],
    "0x8": [0xf0, 0x90, 0xf0, 0x90, 0xf0],
    "0x9": [0xf0, 0x90, 0xf0, 0x10, 0xf0],
    "0xa": [0xf0, 0x90, 0xf0, 0x90, 0x90],
    "0xb": [0xe0, 0x90, 0xe0, 0x90, 0xe0],
    "0xc": [0xf0, 0x80, 0x80, 0x80, 0xf0],
    "0xd": [0xe0, 0x90, 0x90, 0x90, 0xe0],
    "0xe": [0xf0, 0x80, 0xf0, 0x80, 0xf0],
    "0xf": [0xf0, 0x80, 0xf0, 0x80, 0x80]
}


font_list = [
    font["0x0"],
    font["0x1"],
    font["0x2"],
    font["0x3"],
    font["0x4"],
    font["0x5"],
    font["0x6"],
    font["0x7"],
    font["0x8"],
    font["0x9"],
    font["0xa"],
    font["0xb"],
    font["0xc"],
    font["0xd"],
    font["0xe"],
    font["0xf"]
]

# *END DATA*


# *DISPLAY STATES*

ON = pygame.Color(255, 255, 255)
OFF = pygame.Color(0, 0, 0)

# *END DISPLAY STATES*

# *KEYCODES*

supported_keycodes = {
    "48": 0,
    "49": 1,
    "50": 2,
    "51": 3,
    "52": 4,
    "53": 5,
    "54": 6,
    "55": 7,
    "56": 8,
    "57": 9,
    "97": 10,  # 'A'
    "98": 11,  # 'B'
    "99": 12,  # 'C'
    "100": 13,  # 'D'
    "101": 14,  # 'E'
    "102": 15   # 'F'
}

codes_key = {
    "0": 48,
    "1": 49,
    "2": 50,
    "3": 51,
    "4": 52,
    "5": 53,
    "6": 54,
    "7": 55,
    "8": 56,
    "9": 57,
    "10": 97,
    "11": 98,
    "12": 99,
    "13": 100,
    "14": 101,
    "15": 102
}

# *END KEYCODES*


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

# def int_to_bin_str(int_val):
#     bin_str = format(int_val, '08b')
#     return bin_str

def int_to_hex_str(number):
    return hex(number)[2:].zfill(2)



def scaled_draw(x, y, new_pixel_state, surface):
    global V
    x = x * 10
    y = y * 10

    if (new_pixel_state == ON):
        new_pixel_state = True
    else:
        new_pixel_state = False

    
    current_pixel_state = -1

    for pos_x in range(x, x+10):
        for pos_y in range(y, y+10):

            if (surface.get_at((pos_x, pos_y % 320)) == ON):
                current_pixel_state = True
            else:
                current_pixel_state = False
           
            pixel = current_pixel_state != new_pixel_state
            if (pixel):
                surface.set_at((pos_x, pos_y), ON)
            else:
                if (current_pixel_state and new_pixel_state):
                    surface.set_at((pos_x, pos_y), OFF)
                    V[0xF] = 1

def read(addr_idx):
    if addr_idx >= len(memory):  # Fix off-by-one error
        print("Address is larger than memory size")
        return
    return memory[addr_idx]

def load_rom(file_path):
    global memory
    with open(file_path, mode='rb') as file:
        rom_data = file.read()  # Read the whole file as binary data

    for idx in range(len(rom_data)):
        byte = struct.unpack("B", rom_data[idx:idx + 1])[0]
        memory[idx + 0x200] = byte


def load_font(memory):
    flattened_font = [byte for char in font_list for byte in char]
    for i in range(len(flattened_font)):
        if 0x50 + i < len(memory):
            memory[0x50 + i] = flattened_font[i]
        else:
            print(f"Warning: Attempt to write out of memory bounds at address {0x50 + i}")

# *INSTRUCTIONS*

# def CLS(surface):
#     surface.fill(0)
#     pygame.display.flip()

# def LD_VX(Vx, kk):
#     global V
#     Vx = int(Vx, 16)
#     V[Vx] = int(kk, 16)

def LDF_VX(Vx):
    global I
    Vx_value = V[Vx]
    Vx_addr = 0xF * 5 + 0x50
    if Vx_addr is not None:
        if isinstance(Vx_addr, str):
            I = int(Vx_addr, 16)
        else:
            I = Vx_addr

def LDX_VX_15(Vx):
    global delay_timer
    delay_timer = V[Vx]

def LDX_VX(Vx):
    global V
    key = wait_for_keypress()
    V[Vx] = key

def LDX_VX_07(Vx):
    global V
    V[Vx] = delay_timer

def LD_ST(Vx):
    global V
    sound_timer = V[Vx]

def DRW(Vx, Vy, n, surface):
    global V
    mem_slice = memory[I:I+n]
    pos_x = V[Vx] % 64
    pos_y = V[Vy] % 32

    V[0xF] = 0

    binaries = [format(integer, '08b') for integer in mem_slice]
    for binary in binaries:
        for idx in range(8):
            pixel_state = ON if binary[idx] == '1' else OFF                
            if (pos_y > 31 or pos_x + idx > 63):
                break
            scaled_draw(pos_x + idx, pos_y, pixel_state, surface)
        pos_y += 1
    pygame.display.flip()

def JUMP(nnn):
    global pc
    pc = int(nnn, 16)

def JUMPN(nnn):
    global pc
    pc = int(nnn, 16) + V[0]

def SET_I(nnn):
    global I
    I = int(nnn, 16)

def ADD_VX(Vx, nn):
    global V
    V[Vx] = (V[Vx] + int(nn, 16)) % 256

def ADD_I(Vx):
    global I
    I = (V[Vx] + I) % 0x1000

# def RET():
#     global stack, pc
#     if stack:
#         pc = stack.pop()

def CALL(nnn):
    global stack, pc
    stack.append(pc)
    pc = int(nnn, 16)

def SKIP_3(Vx, nn):
    global V, pc
    if V[int(Vx, 16)] == int(nn, 16):
        # increment()
        pc += 0x2

def SKIP_4(Vx, nn):
    global V, pc
    if V[int(Vx, 16)] != int(nn, 16):
        # increment()
        pc += 0x2

def SKIP_5(Vx, Vy):
    global V, pc
    if V[Vx] == V[Vy]:
        pc += 0x2

def SKIP_9(Vx, Vy):
    global V, pc
    if V[Vx] != V[Vy]:
        pc += 0x2

def SKP(Vx):
    global pc
    key_codes = get_keycodes()
    if (codes_key[str(V[Vx])] in key_codes):
        pc += 0x2

def SKNP(Vx):
    global pc
    key_codes = get_keycodes()
    if (codes_key[str(V[Vx])] not in key_codes):
        pc += 0x2

def SUB_5(Vx, Vy):
    global V
    Vx_value = V[Vx]
    Vy_value = V[Vy]
    V[Vx] = (Vx_value - Vy_value) % 256

    V[0xF] = 1
    if Vx_value < Vy_value:
        V[0xF] = 0

def SUB_7(Vx, Vy):
    global V
    Vx_value = V[Vx]
    Vy_value = V[Vy]
    V[Vx] = (Vy_value - Vx_value) % 256

    V[0xF] = 1
    if Vy_value < Vx_value:
        V[0xF] = 0

def OR(Vx, Vy):
    global V
    V[Vx] |= V[Vy]
    V[0xF] = 0

def AND(Vx, Vy):
    global V
    V[Vx] &= V[Vy]
    V[0xF] = 0

def XOR(Vx, Vy):
    global V
    V[Vx] ^= V[Vy]
    V[0xF] = 0

def SHIFT_LEFT(Vx, Vy):
    global V
    V[Vx] = V[Vy]
    old_vx = V[Vx]
    V[Vx] = (V[Vx] << 1) % 256
    V[0xF] = (old_vx >> 7) & 1

def SHIFT_RIGHT(Vx, Vy):
    global V
    V[Vx] = V[Vy]
    old_vx  = V[Vx]
    V[Vx] >>= 1
    V[0xF] = old_vx & 1

def STORE(x):
    global memory, I
    for Vx in range(x + 1):
        memory[I + Vx] = V[Vx]
    I += 1

def LOAD(x):
    global memory, I
    for loc_x in range(x + 1):
        V[loc_x] = memory[I + loc_x]
    I += 1

def RAND(Vx, nn):
    r = random.randint(0, 255)
    V[Vx] = r & int(nn, 16)

def BCD_REP(Vx):
    value = V[Vx]
    memory[I + 2] = value % 10
    value //= 10
    memory[I + 1] = value % 10
    value //= 10
    memory[I] = value % 10

# *END INSTRUCTIONS*

count = 0
def execute_instruction(instruction, surface):
    global count, V, stack, pc, I

    count += 1
    if show_debug_info and count > 900:
        show_resources()

    opcode = instruction[0]

    if instruction == "00E0":
        surface.fill(0)
        pygame.display.flip()
    elif instruction == "00EE":
        pc = stack.pop()
    elif opcode == "6":
        vx = int(instruction[1], 16)
        kk = int(instruction[2:], 16)
        V[vx] = kk
    elif opcode == "7":
        vx = int(instruction[1], 16)
        nn = int(instruction[2:], 16)
        V[vx] = (V[vx] + nn) % 256
    elif opcode == "F":
        vx = int(instruction[1], 16)
        if instruction[2:] == "29":
            vx_addr = 0xF * 5 + 0x50
            if (vx_addr): I = vx_addr
        elif instruction[2:] == "55":
            STORE(vx)
        elif instruction[2:] == "65":
            LOAD(vx)
        elif instruction[2:] == "33":
            BCD_REP(vx)
        elif instruction[2:] == "1E":
            ADD_I(vx)
        elif instruction[2:] == "15":
            LDX_VX_15(vx)
        elif instruction[2:] == "07":
            LDX_VX_07(vx)
        elif instruction[2:] == "0A":
            LDX_VX(vx)
        elif instruction[2:] == "18":
            LD_ST(vx)
    elif opcode == "D":
        vx = instruction[1]
        vy = instruction[2]
        n = instruction[3]
        DRW(int(vx, 16), int(vy, 16), int(n, 16), surface)
    elif opcode == "1":
        nnn = instruction[1:]
        JUMP(nnn)
    elif opcode == "B":
        nnn = instruction[1:]
        JUMPN(nnn)
    elif opcode == "C":
        vx = instruction[1]
        nn = instruction[2:]
        RAND(int(vx, 16), nn)
    elif opcode == "A":
        nnn = instruction[1:]
        SET_I(nnn)
    elif opcode == "2":
        nnn = instruction[1:]
        CALL(nnn)
    elif opcode == "3":
        vx = instruction[1]
        nn = instruction[2:]
        SKIP_3(vx, nn)
    elif opcode == "5":
        vx = instruction[1]
        vy = instruction[2]
        SKIP_5(int(vx, 16), int(vy, 16))
    elif opcode == "4":
        vx = instruction[1]
        nn = instruction[2:]
        SKIP_4(vx, nn)
    elif opcode == "8":
        vx = instruction[1]
        vy = instruction[2]
        subcode = instruction[3]
        if (subcode == "0"):
            V[int(vx, 16)] = V[int(vy, 16)]
        if subcode == "5":
            SUB_5(int(vx, 16), int(vy, 16))
        elif subcode == "7":
            SUB_7(int(vx, 16), int(vy, 16))
        elif subcode == "1":
            OR(int(vx, 16), int(vy, 16))
        elif subcode == "2":
            AND(int(vx, 16), int(vy, 16))
        elif subcode == "4":
            result = V[int(vx, 16)] + V[int(vy, 16)]
            V[int(vx, 16)] = (V[int(vx, 16)] + V[int(vy, 16)]) % 256
            if (result > 255):
                V[0xF] = 1
            else:
                V[0xF] = 0
        elif subcode == "3":
            XOR(int(vx, 16), int(vy, 16))
        elif subcode == "E":
            SHIFT_LEFT(int(vx, 16), int(vy, 16))
        elif subcode == "6":
            SHIFT_RIGHT(int(vx, 16), int(vy, 16))
    elif opcode == "9":
        vx = instruction[1]
        vy = instruction[2]
        subcode = instruction[3]
        SKIP_9(int(vx, 16), int(vy, 16))
    elif opcode == "E":
        vx = instruction[1]
        if (instruction[2:] == "A1"):
            SKNP(int(vx, 16))
        elif (instruction[2:] == "9E"):
            SKP(int(vx, 16))

def get_keycodes():
    keycodes = []
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            keycodes.append(event.key)
    return keycodes

def fetch():
    global pc
    val = memory[pc:pc+2]
    # increment()
    pc += 0x2
    return val

def decode(memory_slice):
    first_byte = int_to_hex_str(memory_slice[0])
    
    if (len(memory_slice) == 2):
        second_byte = int_to_hex_str(memory_slice[1])
        return first_byte + second_byte
    else:
        return first_byte

def cycle(surface):
    instruction = fetch()
    instruction = decode(instruction)
    execute_instruction(instruction.upper(), surface)


clock_speed_hz = 600
cycle_delay = 1.0 / clock_speed_hz

def run():
    global delay_timer, sound_timer
    running = True
 
    pygame.init()
    pygame.key.set_repeat(10, 10)

    pygame.display.set_caption("Chip-8")
    surface = pygame.display.set_mode((640, 320))
    
    pygame.event.clear()
    while running:
        start_time = time.time()
        elapsed_time = time.time() - start_time

        pygame.display.flip()
        cycle(surface)

        if delay_timer > 0:
            delay_timer -= 1

        if sound_timer > 0:
            sound_timer -= 1
        
        if elapsed_time < cycle_delay:
            time.sleep(cycle_delay - elapsed_time)


def print_heading(title):
    print(title)
    print("-" * 40)
    print()
    print()

def get_instruction(pc_address):
    return ''.join(decode(memory[pc_address:pc_address+2]))


def show_resources():
    os.system('clear')

    print_heading("Registers")
    print("I: ", hex(I))
     
    for idx in range(0, len(V)):
        print("V" + str(idx) + ": " + str(V[idx]))
    print()
    print()

    print_heading("Stack")
    for idx in range(0, len(stack)):
        print(str(idx) + ": " + hex(stack[idx]))
    print()
    print()

    print_heading("Program Counter")
    print("Address: " + hex(pc))

    print("Instruction (-2): " + get_instruction(pc - 4).upper())
    print("Instruction (-1): " + get_instruction(pc - 2).upper())
    print("Instruction (c): " + get_instruction(pc).upper())
    print()
    print()


    print_heading("Line Count")

    print("Count: ", count)
    print()
    print()

    # print_heading("Font")
    # print(memory.memory[0x50:0x9F+1])
    print(pc)

    print(memory[0x3d0])
    print(V[0])

    wait_for_keypress()




show_debug_info = False
if len(sys.argv) > 1 and sys.argv[1] == 'debug':
    show_debug_info = True



load_font(memory)


# load_rom("roms/1-chip8-logo.ch8")
# load_rom("roms/2-ibm-logo.ch8")None
load_rom("roms/3-corax.ch8")
# load_rom("roms/4-flags.ch8")
# load_rom("roms/5-quirks.ch8")
# load_rom("roms/6-keypad.ch8")


# load_rom("roms/RPS.ch8")
# load_rom("roms/Airplane.ch8")
# load_rom("roms/Blitz.ch8")
# load_rom("roms/AnimalRace.ch8")
# load_rom("roms/AdditionProblems.ch8")
# load_rom("roms/Pong.ch8")
# load_rom("roms/flightrunner.ch8")

run()
