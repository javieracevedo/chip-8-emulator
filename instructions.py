import display
import registers
import memory
import events
import utils
import pc
import debug
import stack
import sys
import pygame


show_debug_info = False
if (len(sys.argv) > 1 and sys.argv[1] == 'debug'): show_debug_info = True


def CLS(surface):
    surface.fill(0)
    pygame.display.flip()

def LD_VX(Vx, kk):
    Vx = int(Vx, 16)
    registers.V[Vx] = int(kk, 16)

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

    pos_y = registers.V[Vy]
    for integer in mem_slice:
        binary = utils.int_to_bin_str(integer)
        for idx in range(0, 8):
            pixel_state = display.ON
            if (binary[idx] == '0'):
                pixel_state = display.OFF
            display.scaled_draw(registers.V[Vx] + idx, pos_y, pixel_state, surface)
            
        pos_y += 1
    pygame.display.flip()

def JUMP(nnn):
    pc.set(nnn)

def SET_I(nnn):
    registers.I = int(nnn, 16)

def ADD_VX(Vx, nn):
    result = (registers.V[Vx] + int(nn, 16)) % 256
    registers.V[Vx] = result

def ADD_I(Vx):
    registers.I = registers.V[Vx] + registers.I

def RET():
    if (len(stack.stack)):
        addr = stack.stack.pop()
        registers.PC = addr

def CALL(nnn):
    stack.stack.append(pc.pc)
    pc.set(nnn)

def SKIP_3(Vx, nn):
    if (registers.V[Vx] == int(nn, 16)):
        pc.increment()

def SKIP_4(Vx, nn):

    if (registers.V[Vx] != int(nn, 16)):
        pc.increment()

def SKIP_5(Vx, Vy):
    if (registers.V[Vx] == registers.V[Vy]):
        pc.increment()

def SUB_5(Vx, Vy):
    Vx_value = registers.V[Vx]
    Vy_value = registers.V[Vy]

    if (Vx_value > Vy_value):
        registers.V[0xF] = 1
        registers.V[Vx] = Vx_value - Vy_value
    else:
        registers.V[0xF] = 0
        registers.V[Vx] = (Vx_value - Vy_value) % 256
 

def SUB_7(Vx, Vy):
    Vx_value = registers.V[Vx]
    Vy_value = registers.V[Vy]

    if (Vy_value > Vx_value):
        registers.V[0xF] = 1
        registers.V[Vx] = Vy_value - Vx_value
    else:
        registers.V[0xF] = 0
        registers.V[Vx] = (Vy_value - Vx_value) % 256

def OR(Vx, Vy):
    Vx_value = registers.V[Vx]
    Vy_value = registers.V[Vy]

    registers.V[Vx] = Vx_value | Vy_value
 
def AND(Vx, Vy):
    Vx_value = registers.V[Vx]
    Vy_value = registers.V[Vy]

    registers.V[Vx] = Vx_value & Vy_value

def XOR(Vx, Vy):
    Vx_value = registers.V[Vx]
    Vy_value = registers.V[Vy]

    registers.V[Vx] = Vx_value ^ Vy_value

def SHIFT_LEFT(Vx):
    Vx_value = registers.V[Vx]
    msb = bin(Vx_value)[2]
    if (Vx_value <= 127):
       registers.V[0xF] = 0 
    else:
        registers.V[0xF] = int(msb)
    registers.V[Vx] = Vx_value << 1

def SHIFT_RIGHT(Vx):
    Vx_value = registers.V[Vx]
    msb = int(bin(Vx_value)[-1])
    registers.V[15] = msb
    registers.V[Vx] = Vx_value >> 1

def STORE(x):
    for Vx in range(0, x+1):
        print(Vx)
        memory.memory[registers.I + Vx] = registers.V[Vx]


def LOAD(x):
    for loc_x in range(0, x+1):
        registers.V[loc_x] = memory.memory[registers.I + loc_x]



def BCD_REP(Vx):
    value = registers.V[Vx]

    print(memory.memory[976:982])

    memory.write(registers.I, value % 10)
    value = value // 10

    memory.write(registers.I + 1, value % 10)
    value = value // 10

    memory.write(registers.I + 2, value)


    print(memory.memory[976:982])


 
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
        elif (instruction[2:] == "55"):
            x_range = instruction[1]
            STORE(int(x_range, 16))
        elif (instruction[2:] == "65"):
            x_range = instruction[1]
            LOAD(int(x_range, 16))
        elif (instruction[2:] == "33"):
            Vx = instruction[1]
            #BCD_REP(int(Vx, 16))
        elif (instruction[2:] == "1E"):
            Vx = instruction[1]
            ADD_I(int(Vx, 16))
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
        SET_I(nnn)
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
    elif (instruction[0] == "8" and instruction[3] == "3"):
        Vx = instruction[1]
        Vy = instruction[2]
        XOR(int(Vx, 16), int(Vy, 16))
    elif (instruction[0] == "8" and instruction[3] == "E"):
        Vx = instruction[1]
        SHIFT_LEFT(int(Vx, 16))
    elif (instruction[0] == "8" and instruction[3] == "6"):
        Vx = instruction[1]
        SHIFT_RIGHT(int(Vx, 16))
            

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
