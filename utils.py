def hex_to_bin(hex_val):
    int_val = int(hex_val, 16);
    bin_str = format(int_val, '08b')
    return bin_str

