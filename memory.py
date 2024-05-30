MEM_SIZE_BYTES=12
memory = []
alloc_table = []


def is_hex(s):
    try:
        int(s, 16)
        return True
    except ValueError:
        return False

def init():
    for i in range(MEM_SIZE_BYTES):
        memory.append(0x0)

def write(addr_idx, hex_data, alloc=True):
    if (not is_free(addr_idx)):
        print("This memory address is not free for use (addr: ", addr_idx, ")")
        return;

    # Check if hex_data is actually hex
    if (not is_hex(str(hex_data))):
        print("Hex data argument is not hex")
        return;
   
    # Check if hex only has two digits
    if (hex_data > 0xFF):
        print("Hex data cannot be more than 2 digits")
        return;

    memory[addr_idx] = hex_data
    if (alloc):
        alloc_table.append(addr_idx)
    
def read(addr_idx):
    if (addr_idx > len(memory)):
        print("Address is larger than memory size")
        return;
    print(memory[addr_idx])
    return memory[addr_idx]

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


