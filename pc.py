import memory

# 12-bit program counter
pc = 0x200

def set(nibble):
    if nibble >= memory.MEM_SIZE_BYTES:
        print("This function only accepts a 3-nibble (12-bit) address.")
        return

    global pc 
    pc = nibble

def increment():
    global pc
    if pc + 0x2 < memory.MEM_SIZE_BYTES:
        pc += 0x2
    else:
        print("Program counter exceeded memory bounds.")

