# Chip-8 Virtual Machine

This is my implementation of the CHIP-8 virtual machine from the 1970s. I started working on this for fun on the weekend, not thinking I would decide to follow through, so it is a quick and dirty implementation, at least for now.


## VM Description

### Memory

The CHIP-8 VM has 4096 addresses. Each contains 8 bits, for a total of 4KB of space. The first 512 bytes were reserved for the interpreter, this is no longer necessary since the interpreter can run natively in the host. Modern implementations (like this one) store font data in that space. The last 256 bytes are reserved for display refresh and the previous 96 bytes before that are reserved for the call stack, internal use, and other variables.


### Registers

The CHIP-8 has 16 registers (V0...VF). VF is typically used for addition and no borrow flags. Additionally, an address register (I) stores a 12-bit wide address (4096 addresses in total). 


### Font

The CHIP-8 virtual machine has a built-in font. It has the characters 0 through F. Here are the character sprite specs:

![alt text](font.jpeg "Chip-8 Font Specs")


### Display

The display is 64x32 pixels tall (however in this implementation it's scaled). To handle graphics I'm using the SDL wrapper for python: pygame.


### Stack

The stack is used to store return addresses when subroutines are called. In the old days the stack allowed 12 levels of nesting, in modern implementations this limitation doesn't exist.


### Timers

1. Delay timer
2. Sound timer


### Opcode table

| Opcode        | Instruction                                              |
| ------------  | -------------------------------------------------------- |
| 00E0          | Clear screen                                             |
| 1NNN          | Jump                                                     |               
| 6XNN          | Set VX to NN                                             |
| 7XNN          | Add NN to VX                                             |
| ANNN          | Set I to NNN                                             |
| DXYN          | Display the value in memory location I at VX VY position |
| 0NNN          | Pause execution and execute the instruction in NNN       |
| 2NNN          | Push PC to the stack and call subroutine at NNN          |
| 00EE          | Return from subroutine (pop last address from stack)     | 
| 3XNN          | Conditional skip                                         |
| 4XNN          | Conditional skip                                         |
| 5XY0          | Conditional skip                                         |
| 9XY0          | Conditional skip                                         |
| 6XNN          | Set VX to NN                                             |
| 7XNN          | Add NN to VX                                             |
| 8XY0          | Set VX to the value of VY                                |
| 8XY1          | Set VX to the result of VX || VY                         |
| 8XY2          | Set VX to the result of VX && VY                         |
| 8XY3          | Set VX to the result of VX ^  VY                         |       
| 8XY4          | Set VX to the result of VX + VY (Add)                    | 
| 8XY5/8XY7     | Set VX to the result of VX - VY (Subtract)               |
| 8XY6/8XYE     | Shift the value of VX one bit to the right or left       |
| BXNN          | Jump to address XNN plus the value in VX                 |
| CXNN          | Generates a random number and binary ANDs it with NN     |
| EX9E/EXA1     | Skip the next instruction if a key is being pressed      |
| FX07/FX15/FX18| Timers                                                   |
| FX55/FF66     | Store/Load registers to/from memory                      |
| FX33          | Converts the value in VX to three decimal digits and stores them in the address in I |
| FX1E          | Add the value of VX to I                                 |
| FX0A          | Wait for keypress                                        |
| FX29          | Set I to the address of the hex value in VX              |


