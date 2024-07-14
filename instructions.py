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

count = 0

show_debug_info = False
if len(sys.argv) > 1 and sys.argv[1] == 'debug':
    show_debug_info = True

def CLS(surface):
    surface.fill(0)
    pygame.display.flip()

def LD_VX(Vx, kk):
    Vx = int(Vx, 16)
    registers.V[Vx] = int(kk, 16)

def LDF_VX(Vx):
    Vx_value = registers.V[Vx]
    Vx_addr = memory.get_font_addr(Vx_value)
    if Vx_addr is not None:
        if isinstance(Vx_addr, str):
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
        for idx in range(8):
            pixel_state = display.ON if binary[idx] == '1' else display.OFF
            display.scaled_draw(registers.V[Vx] + idx, pos_y, pixel_state, surface)
        pos_y += 1
    pygame.display.flip()

def JUMP(nnn):
    pc.set(int(nnn, 16))

def SET_I(nnn):
    registers.I = int(nnn, 16)

def ADD_VX(Vx, nn):
    registers.V[Vx] = (registers.V[Vx] + int(nn, 16)) % 256

def ADD_I(Vx):
    registers.I = (registers.V[Vx] + registers.I) % 0x1000

def RET():
    if stack.stack:
        addr = stack.stack.pop()
        pc.set(addr)

def CALL(nnn):
    stack.stack.append(pc.pc)
    pc.set(int(nnn, 16))

def SKIP_3(Vx, nn):
    if registers.V[Vx] == int(nn, 16):
        pc.increment()

def SKIP_4(Vx, nn):
    if registers.V[Vx] != int(nn, 16):
        pc.increment()

def SKIP_5(Vx, Vy):
    if registers.V[Vx] == registers.V[Vy]:
        pc.increment()

def SUB_5(Vx, Vy):
    Vx_value = registers.V[Vx]
    Vy_value = registers.V[Vy]
    if Vx_value > Vy_value:
        registers.V[0xF] = 1
    else:
        registers.V[0xF] = 0
    registers.V[Vx] = (Vx_value - Vy_value) % 256

def SUB_7(Vx, Vy):
    Vx_value = registers.V[Vx]
    Vy_value = registers.V[Vy]
    if Vy_value > Vx_value:
        registers.V[0xF] = 1
    else:
        registers.V[0xF] = 0
    registers.V[Vx] = (Vy_value - Vx_value) % 256

def OR(Vx, Vy):
    registers.V[Vx] |= registers.V[Vy]

def AND(Vx, Vy):
    registers.V[Vx] &= registers.V[Vy]

def XOR(Vx, Vy):
    registers.V[Vx] ^= registers.V[Vy]

def SHIFT_LEFT(Vx):
    Vx_value = registers.V[Vx]
    registers.V[0xF] = (Vx_value >> 7) & 1
    registers.V[Vx] = (Vx_value << 1) % 256

def SHIFT_RIGHT(Vx):
    Vx_value = registers.V[Vx]
    registers.V[0xF] = Vx_value & 1
    registers.V[Vx] >>= 1

def STORE(x):
    for Vx in range(x + 1):
        memory.memory[registers.I + Vx] = registers.V[Vx]

def LOAD(x):
    for loc_x in range(x + 1):
        registers.V[loc_x] = memory.memory[registers.I + loc_x]

def BCD_REP(Vx):
    value = registers.V[Vx]
    memory.write(registers.I + 2, value % 10)
    value //= 10
    memory.write(registers.I + 1, value % 10)
    value //= 10
    memory.write(registers.I, value)

def execute_instruction(instruction, surface):
    if show_debug_info:
        debug.show_resources()

    opcode = instruction[0]
    if instruction == "00E0":
        CLS(surface)
    elif instruction == "00EE":
        RET()
    elif opcode == "6":
        vx = instruction[1]
        kk = instruction[2:]
        LD_VX(vx, kk)
    elif opcode == "7":
        vx = instruction[1]
        nn = instruction[2:]
        ADD_VX(int(vx, 16), nn)
    elif opcode == "F":
        vx = instruction[1]
        if instruction[2:] == "29":
            LDF_VX(int(vx, 16))
        elif instruction[2:] == "55":
            STORE(int(vx, 16))
        elif instruction[2:] == "65":
            LOAD(int(vx, 16))
        elif instruction[2:] == "33":
            BCD_REP(int(vx, 16))
        elif instruction[2:] == "1E":
            ADD_I(int(vx, 16))
        else:
            LDX_VK(int(vx, 16))
    elif opcode == "D":
        vx = instruction[1]
        vy = instruction[2]
        n = instruction[3]
        DRW(int(vx, 16), int(vy, 16), int(n, 16), surface)
    elif opcode == "1":
        nnn = instruction[1:]
        JUMP(nnn)
    elif opcode == "A":
        nnn = instruction[1:]
        SET_I(nnn)
    elif opcode == "2":
        nnn = instruction[1:]
        CALL(nnn)
    elif opcode == "3":
        vx = instruction[1]
        nn = instruction[2:]
        SKIP_3(int(vx, 16), nn)
    elif opcode == "5":
        vx = instruction[1]
        vy = instruction[2]
        SKIP_5(int(vx, 16), int(vy, 16))
    elif opcode == "4":
        vx = instruction[1]
        nn = instruction[2:]
        SKIP_4(int(vx, 16), nn)
    elif opcode == "8":
        vx = instruction[1]
        vy = instruction[2]
        subcode = instruction[3]
        if subcode == "5":
            SUB_5(int(vx, 16), int(vy, 16))
        elif subcode == "7":
            SUB_7(int(vx, 16), int(vy, 16))
        elif subcode == "1":
            OR(int(vx, 16), int(vy, 16))
        elif subcode == "2":
            AND(int(vx, 16), int(vy, 16))
        elif subcode == "3":
            XOR(int(vx, 16), int(vy, 16))
        elif subcode == "E":
            SHIFT_LEFT(int(vx, 16))
        elif subcode == "6":
            SHIFT_RIGHT(int(vx, 16))

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
