import data
import numpy as np
import struct
import utils


MEM_SIZE_BYTES=4096
memory = []
alloc_table = []


def is_hex(s):
    try:
        int(s, 16)
        return True
    except ValueError:
        return False

def init():
    for _ in range(MEM_SIZE_BYTES):
        memory.append(0)

def write(addr_idx, value, alloc=True):
    if (len(memory) == 0):
        print("Memory has not been initialized...")
        return

    if (not is_free(addr_idx)):
        print("This memory address is not free for use (addr: ", addr_idx, ")")
        return

    if (not isinstance(value, int)):
        print("Value should be a number")
        return

    if (value > 255):
        print("Value cannot be larger than 1 byte.")
        return

    if (addr_idx > MEM_SIZE_BYTES):
        print("Addr_idx larger than memory")
        return

    memory[addr_idx] = value
    if (alloc):
        alloc_table.append(addr_idx)
    
def read(addr_idx):
    if (addr_idx > len(memory)):
        print("Address is larger than memory size")
        return
    return memory[addr_idx]

def get_font_addr(value):
    for idx in range(0x50, 0x9F + 1, 5):
        if (data.font[hex(value)] == memory[idx:idx+5]):
            return idx
    return None

def get_addr(value):
    for idx in range(len(memory)):
        if value == memory[idx] and not is_free(value):
            return idx
    return -1

def is_free(addr_idx):
    return not (addr_idx in alloc_table)

def free(addr_idx):
    if is_free(addr_idx): return
    del alloc_table[addr_idx]
    write(addr_idx, 0x0, alloc=False)

def load_rom(file_path):
    with open(file_path, mode='rb') as file:
        lines = file.readlines()
        lines = np.array(lines).flatten()[0]
    
        for idx in range(0, len(lines)):
            byte = struct.unpack("B", lines[idx:idx+1])[0]
            write(idx + 0x200, byte)

