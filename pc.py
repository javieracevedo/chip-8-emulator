import memory

# 12 bit
pc = None


def set(nibble):
    if (int(nibble, 16) > memory.MEM_SIZE_BYTES):
        print("This function only accepts a 3 nibbles (12 bits)")
        return

    global pc 
    pc = hex(int(nibble, 16))



