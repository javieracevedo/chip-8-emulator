
arr = ['0xf0', '0x90', '0x90', '0x90', '0xf0']



def hex_to_bin(hex_val):
    hex_val = int(hex_val, 16);
    hex_val = bin(hex_val)
    return hex_val


