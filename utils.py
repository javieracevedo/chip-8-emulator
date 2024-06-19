def int_to_bin_str(int_val):
    bin_str = format(int_val, '08b')
    return bin_str

def int_to_hex_str(number):
    return hex(number)[2:].upper()