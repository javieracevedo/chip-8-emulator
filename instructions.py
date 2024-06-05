import display
import registers
import memory
import events
import pygame
import utils
import pc


def CLS(surface):
    surface.fill(0)
    pygame.display.flip()

def LD_VX(Vx, kk):
    Vx = int(Vx)
    registers.V[Vx] = hex(int(kk, 16))

def LDF_VX(Vx):
    Vx_value = registers.V[Vx]
    Vx_addr = memory.get_font_addr(Vx_value)
    if (Vx_addr != None):
        registers.I = Vx_addr

def LDX_VK(Vx):
    key = events.wait_for_keypress();
    registers.V[Vx] = key


def DRW(Vx, Vy, n, surface):
    mem_slice = memory.memory[registers.I:registers.I+n]

    pos_y = int(registers.V[Vy], 16)
    for hex_str in mem_slice:
        binary = utils.hex_to_bin(hex_str)
        for idx in range(0, 8):
            pixel_state = display.ON
            if (binary[idx] == '0'):
                pixel_state = display.OFF
            display.scaled_draw(int(registers.V[Vx], 16) + idx, pos_y, pixel_state, surface);
            
        pos_y += 1
    pygame.display.flip()

def JUMP(nnn):
    pc.set(nnn)

def SET_I(nnn):
    registers.I = nnn


def ADD_VX(Vx, nn):
    result = str((int(registers.V[Vx], 16) + int(nn, 16)) % 256)
    registers.V[Vx] = result


def execute_instructions(instructions, surface):
    for c in range(len(instructions)):
        instruction = instructions[c]
        if (instruction == "00E0"):
            CLS(surface)
        elif (instruction[0] == "6"):
            vx = instruction[1]
            kk = instruction[2:]
            LD_VX(vx, kk)
        elif (instruction[0] == "7"):
            vx = instruction[1]
            nn = instruction[2:]
            ADD_VX(int(vx), nn)
        elif (instruction[0] == "F"):
            print("here")
            vx = instruction[1]
            if (instruction[2:] == "29"):
                LDF_VX(int(vx, 16))
            else:
                LDX_VK(int(vx, 16))
        elif (instruction[0] == "D"):
            vx = instruction[1]
            vy = instruction[2]
            n = instruction[3]
            DRW(int(vx, 16), int(vy, 16), int(n, 16), surface)
        elif (instruction[0] == "1"):
            nnn = instruction[1:]
            JUMP(nnn)
        elif (instruction[0] == "A"):
            nnn = instruction[1:]
            SET_I(int(nnn, 16))


