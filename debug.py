import os
import registers
import events
import pc
import memory
import stack
import instructions

def print_heading(title):
    print(title)
    print("-" * 40)
    print()
    print()

def get_instruction(pc_address):
    return ''.join(instructions.decode(memory.memory[pc_address:pc_address+2]))


def show_resources():
    os.system('clear')

    print_heading("Registers")
    print("I: ", hex(registers.I))
     
    for idx in range(0, len(registers.V)):
        print("V" + str(idx) + ": " + str(registers.V[idx]))
    print()
    print()

    print_heading("Stack")
    for idx in range(0, len(stack.stack)):
        print(str(idx) + ": " + hex(stack.stack[idx]))
    print()
    print()

    print_heading("Program Counter")
    print("Address: " + hex(pc.pc))

    print("Instruction (-2): " + get_instruction(pc.pc - 4).upper())
    print("Instruction (-1): " + get_instruction(pc.pc - 2).upper())
    print("Instruction (c): " + get_instruction(pc.pc).upper())
    print()
    print()

    # print_heading("Font")
    # print(memory.memory[0x50:0x9F+1])
    print(pc.pc)

    print(memory.memory[0x3d0])
    print(registers.V[0])

    events.wait_for_keypress()


