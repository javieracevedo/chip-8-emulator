import pygame




mem = []
WORD_SIZE = 8
MEM_SIZE_KB = 4096
ADDRESSES = 2 ** WORD_SIZE


# Later this could be an actual address, instead of a tuple?
I_REG = ()


V = [
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00
]

alloc_table_indexes = []


pygame.init()
pygame.display.set_caption("minimal program")
screen = pygame.display.set_mode((640, 320))




instructions = [
    "00E0",  # Clear the screen
    "6000",  # Set X co-ordinate
    "6100",  # Set Y co-ordinate
    "6201",  # Put number V2
    "F229",  # Stores the address of V2 into I
    "D015"   # Draw 5 bytes(sprite) at V0,V1 position, starting at the value that V2 points to.
]

def get_addr(value):
    for i in range(0, 512, 40):
        font_val = mem[i:i+40]
        if (font_val[0] != 0):
            str_font_val = ''.join(mem[i:i+40])
            if (str_font_val == value):
                return (i, i+40)
    return ()

def CLS():
    "Clear the screen."
    screen.fill(0)
    #print("(CLS)")

def LD_VX(Vx, kk):
    #print(kk)
    Vx = int(Vx)
    V[Vx] = kk 

def LDF_VX(Vx):
    "Find the address of the value stored in Vx and store it in V2."
    Vx_value = V[Vx]
    print("Vx_value: ", hex(Vx_value))
    Vx_addr = get_addr(Vx_value)
    if (Vx_addr != ()):
        I_REG = Vx_addr
    #print("(LDF) Vx:", Vx)

def DRW(Vx, Vy):
    "Draw 5 bytes (sprite) at Vx, Vy position, starting at the value that V2 points to."
    pass
    #print("(DRW) Vx:", Vx, "Vy:", Vy)


def execute_instructions():
    for c in range(len(instructions)):
        ins = instructions[c]
        if (ins == "00E0"):
            CLS()
        elif (ins[0] == "6"):
            vx = ins[1]
            kk = ins[2:]
            LD_VX(vx, kk)
        elif (ins[0] == "F"):
            vx = ins[1]
            LDF_VX(int(vx))
        elif (ins[0] == "D"):
            vx = ins[1]
            vy = ins[2]
            DRW(vx, vy)


#execute_instructions()


#print(V)




def scaled_draw(x, y, surface):
    x = x * 10
    y = y * 10

    for pos_x in range(x, x+10):
        for pos_y in range(y, y+10):
            surface.set_at((pos_x, pos_y), pygame.Color(255, 255, 255))


def main():
    
    running = True
    
    
    CLS()


    #execute_instructions()
    while running:
        scaled_draw(40, 31, screen)
        scaled_draw(10, 3, screen)
       
        #screen.set_at((40, 100), pygame.Color(255, 255, 255))
        
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


ONE="11110000   10010000  10010000 10010000 11110000"
TWO="00100000   01100000   00100000 00100000 01110000"
THREE="11110000 00010000 11110000 10000000 11110000"
FOUR="10010000  10010000  11110000  00010000 00010000"
FIVE="11110000  10000000  11110000  00010000 11110000"
SIX=" 11110000  10000000   11110000   10010000 11110000"

FONT = ONE+TWO+THREE+FOUR+FIVE+SIX



#    <---unused--->
PC = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

def is_free(addrA):
    addr_range = (addrA, addrA+WORD_SIZE)
    for i in range(len(alloc_table_indexes)):
        if (addr_range == alloc_table_indexes[i]):
            return False
    return True

def free(addrA):
    if (is_free(addrA)):
        print("Memory already freed")
        return

    addr_range = (addrA, addrA+WORD_SIZE)
    for i in range(0, len(alloc_table_indexes)):
        if (addr_range == alloc_table_indexes[i]):
            del alloc_table_indexes[i]
            #print("Addr is", addrA,"freeeeeeeeeeee!")
            break
    
    write(addrA, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], alloc=False)
    
def write(addrA, data, alloc=True):
    if (not is_free(addrA)):
        print("This memory addr range is not free or your are not meant to be using this...scoundrel. ( addr",  addrA, ")")
        return

    if (len(data) != WORD_SIZE):
        print("Data is not the right size, not changing shittttt")
        return

    if (addrA % WORD_SIZE != 0):
        print("Misaligned address")
        return
    
    for i in range(addrA, addrA + WORD_SIZE):
        mem[i] = data[i - addrA]

    #print("Wrote stuff weeee at addr: ", addrA)
    if (alloc):
        alloc_table_indexes.append((addrA, addrA+WORD_SIZE))

def init_mem():
    for _ in range(0, MEM_SIZE_KB * 8):
        mem.append(0x00)

def read(addrA):
    if (addrA > len(mem) * 8):
        print("Wtf are you trying to do, you piece of shit")
        return
    
    if (addrA % WORD_SIZE != 0):
        print("Misaligned address")
        return
    

    print(mem[addrA:addrA+WORD_SIZE])

def get_addr(value):
    for i in range(0, 512, 40):
        font_val = mem[i:i+40]
        if (font_val[0] != 0):
            str_font_val = ''.join(mem[i:i+40])
            if (str_font_val == value):
                return (i, i+40)
    return ()
def add_interpreter():
    pass


init_mem()
execute_instructions()
#print(len(FONT))



write(512,[1, 1, 1, 1, 1, 1, 1, 1]) 
write(520, [1, 1, 1, 1, 1, 1, 1, 1])


for x in range(0, len(FONT), 8):
    write(x, FONT[x:x+8])  


print(V)
print(I_REG)

#if __name__ == "__main__":
#    main()
