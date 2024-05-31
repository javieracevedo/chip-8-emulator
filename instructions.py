import display
import registers
import memory
import events

def CLS(surface):
    surface.fill(0)

def LD_VX(Vx, kk):
    Vx = int(Vx)
    registers.V[Vx] = kk

def LDF_VX(Vx):
    Vx_value = registers.V[Vx]
    Vx_addr = memory.get_addr(Vx_value)
    if (Vx_addr != ()):
        registers.I = Vx_addr

def LDX_VK(Vx):
    key = events.wait_for_keypress();
    registers.V[Vx] = key

def DRW(Vx, Vy, surface):
    display.scaled_draw(int(registers.V[Vx]), int(registers.V[Vy]), surface);

def execute_instructions(instructions, surface):
    for c in range(len(instructions)):
        instruction = instructions[c]
        if (instruction == "00E0"):
            CLS(surface)
        elif (instruction[0] == "6"):
            vx = instruction[1]
            kk = instruction[2:]
            LD_VX(vx, kk)
        elif (instruction[0] == "F"):
            vx = instruction[1]
            if (instruction[2:] == "29"):
                LDF_VX(int(vx))
            else:
                LDX_VK(int(vx))
        elif (instruction[0] == "D"):
            vx = instruction[1]
            vy = instruction[2]
            DRW(int(vx), int(vy), surface)

