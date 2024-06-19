import display
import registers
import memory
import events
import pygame
import utils
import pc
import debug
import stack
import sys



show_debug_info = False
if (len(sys.argv) > 1 and sys.argv[1] == 'debug'): show_debug_info = True


def CLS(surface):
    surface.fill(0)
    pygame.display.flip()

def LD_VX(Vx, kk):
    Vx = int(Vx, 16)
    registers.V[Vx] = hex(int(kk, 16))

def LDF_VX(Vx):
    Vx_value = registers.V[Vx]
    Vx_addr = memory.get_font_addr(Vx_value)
    if (Vx_addr != None):
        if (type(Vx_addr) == str):
            registers.I = int(Vx_addr, 16)
        else:
            registers.I = Vx_addr
def LDX_VK(Vx):
    key = events.wait_for_keypress()
    registers.V[Vx] = key

def DRW(Vx, Vy, n, surface):
    mem_slice = memory.memory[registers.I:registers.I+n]

    pos_y = int(registers.V[Vy], 16)
    for integer in mem_slice:
        binary = utils.int_to_bin_str(integer)
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
    result = (int(registers.V[Vx], 16) + int(nn, 16)) % 256
    registers.V[Vx] = hex(result)

def RET():
    if (len(stack.stack)):
        addr = stack.stack.pop()
        registers.PC = addr

def CALL(nnn):
    stack.stack.append(pc.pc)
    pc.set(nnn)


def SKIP_3(Vx, nn):
    print("SKip: " + registers.V[Vx] + "nn: " + nn)
    if (registers.V[Vx].upper()[2:] == nn):
        pc.increment()

def SKIP_4(Vx, nn):
    if (registers.V[Vx].upper()[2:] != nn):
        pc.increment()

def SKIP_5(Vx, Vy):
    if (registers.V[Vx] == registers.V[Vy]):
        pc.increment()


def SUB_5(Vx, Vy):
    Vx_value = int(registers.V[Vx], 16)
    Vy_value = int(registers.V[Vy], 16)

    print("Vx val:" + str(Vx_value))
    print("Vy val: " + str(Vy_value))

    if (Vx_value > Vy_value):
        registers.V[0xF] = '0x01'
        registers.V[Vx] = hex(Vx_value - Vy_value)
    else:
        registers.V[0xF] = '0x00'
        registers.V[Vx] = hex((Vx_value - Vy_value) % 256)
    print("Stuff: ", registers.V)
        

def SUB_7(Vx, Vy):
    Vx_value = int(registers.V[Vx], 16)
    Vy_value = int(registers.V[Vy], 16)

    print("Vx val:" + str(Vx_value))
    print("Vy val: " + str(Vy_value))

    if (Vy_value > Vx_value):
        registers.V[0xF] = '0x01'
        registers.V[Vx] = hex(Vy_value - Vx_value)
    else:
        registers.V[0xF] = '0x00'
        registers.V[Vx] = hex((Vy_value - Vx_value) % 256)
    print("Stuff: ", registers.V)

def OR(Vx, Vy):
    Vx_value = int(registers.V[Vx], 16)
    Vy_value = int(registers.V[Vy], 16)

    registers.V[Vx] = hex(Vx_value | Vy_value)
 
def AND(Vx, Vy):
    Vx_value = int(registers.V[Vx], 16)
    Vy_value = int(registers.V[Vy], 16)

    print("VX: ", Vx_value)
    print("VY: ", Vy_value)

    registers.V[Vx] = hex(Vx_value & Vy_value)

def execute_instruction(instruction, surface):
    if show_debug_info:
        debug.show_resources()


    if (instruction == "00E0"):
        CLS(surface)
    elif (instruction == "00EE"):
        RET()
    elif (instruction[0] == "6"):
        vx = instruction[1]
        kk = instruction[2:]
        LD_VX(vx, kk)
    elif (instruction[0] == "7"):
        vx = instruction[1]
        nn = instruction[2:]
        ADD_VX(int(vx), nn)
    elif (instruction[0] == "F"):
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
    elif (instruction[0] == "2"):
        nnn = instruction[1:]
        CALL(nnn)
    elif (instruction[0] == "3"):
        Vx = instruction[1]
        nn = instruction[2:]
        SKIP_3(int(Vx, 16), nn)
    elif (instruction[0] == "5"):
        Vx = instruction[1]
        Vy = instruction[2]

        SKIP_5(int(Vx, 16), int(Vy))
    elif (instruction[0] == "4"):
        Vx = instruction[1]
        nn = instruction[2:]
        SKIP_4(int(Vx), nn)

    elif (instruction[0] == "8" and instruction[3] == "5"):
        Vx = instruction[1]
        Vy = instruction[2]
        SUB_5(int(Vx), int(Vy))
    elif (instruction[0] == "8" and instruction[3] == "7"):
        Vx = instruction[1]
        Vy = instruction[2]
        SUB_7(int(Vx, 16), int(Vy, 16))
    elif (instruction[0] == "8" and instruction[3] == "1"):
        Vx = instruction[1]
        Vy = instruction[2]
        OR(int(Vx, 16), int(Vy, 16))
    elif (instruction[0] == "8" and instruction[3] == "2"):
        Vx = instruction[1]
        Vy = instruction[2]
        AND(int(Vx, 16), int(Vy, 16))


def fetch():
    pc.increment()
    return memory.memory[pc.pc:pc.pc+2]

def decode(memory_slice):
    first_byte = utils.int_to_hex_str(memory_slice[0])
    second_byte = utils.int_to_hex_str(memory_slice[1])

    return first_byte + second_byte


def cycle(surface):
    instruction = fetch()
    instruction = decode(instruction)
    execute_instruction(instruction.upper(), surface)
