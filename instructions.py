import display
import registers
import memory
import events
import pygame
import utils

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

def DRW(Vx, Vy, surface):
    # Draw the sprite at I addr
    #print("Wohoo: ", registers.I)
    mem_slice = memory.memory[registers.I:registers.I+5]
    pos_y = int(registers.V[Vy], 16)
    for hex_str in mem_slice:
        binary = utils.hex_to_bin(hex_str)
        for idx in range(2, 6):
            pixel_state = display.ON
            if (binary[idx] == '0'):
                pixel_state = display.OFF
            print("Pixel State: ", pixel_state)
            display.scaled_draw(int(registers.V[Vx], 16) + idx - 2, pos_y, pixel_state, surface);
            
        print()
        pos_y += 1
    pygame.display.flip()

def execute_instructions(instructions, surface):
    for c in range(len(instructions)):
        instruction = instructions[c]
        if (instruction == "00E0"):
            CLS(surface)
        elif (instruction[0] == "6"):
            vx = instruction[1]
            kk = instruction[2:]
            LD_VX(vx, kk)
        elif (instruction[0] == "F"):
            vx = instruction[1]
            if (instruction[2:] == "29"):
                LDF_VX(int(vx))
            else:
                LDX_VK(int(vx))
        elif (instruction[0] == "D"):
            vx = instruction[1]
            vy = instruction[2]
            DRW(int(vx), int(vy), surface)

