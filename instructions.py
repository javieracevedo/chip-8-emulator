import display
import registers

#     <-Unused->
PC = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


def CLS(surface):
    surface.fill(0)


def LD_VX(Vx, kk):
    Vx = int(Vx)
    registers.V[Vx] = kk

def LDF_VX(Vx):
    Vx_value = V[Vx]
    print("Vx_value: ", hex(Vx_value))
    Vx_addr = get_addr(Vx_value)
    if (Vx_addr != ()):
        register.I = Vx_addr

def DRW(Vx, Vy):
    pass

def execute_instructions():
    for c in range(len(instructions)):
        instruction = instructions[c]
        if (instruction == "00E0"):
            CLS()
        elif (instruction[0] == "6"):
            vx = instruction[1]
            kk = instruction[2:]
            LD_VX(vx, kk)
        elif (instruction[0] == "F"):
            vx = instruction[1]
            LDF_VX(int(vx))
        elif (instruction[0] == "D"):
            vx = instruction[1]
            vy = instruction[2]
            DRW(vx, vy)


