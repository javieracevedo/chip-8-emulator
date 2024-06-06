import os
import registers
import events


def print_heading(title):
    print(title)
    print("-" * 40)
    print()
    print()


def show_resources():
    os.system('clear')

    print_heading("Registers")
    print("I: ", hex(registers.I))
     
    for idx in range(0, len(registers.V)):
        print("V" + str(idx) + ": " + str(registers.V[idx]))
    print()
    print()

    print_heading("Stack")
    print_heading("Program Counter")
    events.wait_for_keypress()
    
