import memory

# 12 bit
pc = 0x200


def set(nibble):
    if (int(nibble, 16) > memory.MEM_SIZE_BYTES):
        print("This function only accepts a 3 nibbles (12 bits)")
        return

    global pc 
    pc = int(nibble, 16)


def increment():
    global pc
    if pc <= 4096:
        pc += 0x2

