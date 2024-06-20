import os
import registers
import events
import pc
import memory
import stack

def print_heading(title):
    print(title)
    print("-" * 40)
    print()
    print()

def get_instruction(pc_address):
    instruction = ''
    if (type(memory.memory[pc_address]) == str):
        instruction = ''.join(memory.memory[pc_address:pc_address+2])
    
    return instruction 

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
    print("Instruction: " + get_instruction(pc.pc).upper())
    events.wait_for_keypress()


