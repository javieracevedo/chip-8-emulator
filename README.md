# Chip-8 Virtual Machine

This is my implementation of the CHIP-8 virtual machine from the 1970s.


## VM Description

### Memory


1. 4096 Addresses, each containing 8 bits.
2. The first 512 bytes are reserved for the interpreter (this is not necessary in modern implementations of the VM, since the interpreter can run natively in the host, this space is used to storre the font instead)
3. The last 256 bytes are reserved for display refresh.
4. Address range 0xEA0 -> 0xEFF are reserved for the call stack, internal use and variables. 


### Registers

1. 16 Registers named V0...VF.
    1. VF is typically used for flags (addition, no borrow flags).
2. The address register (I), is 12 bits wide (4096 adddresses), it's used to store memory addresses locations.



### Font

TODO

### Display

TODO

### Stack

The stack is used to store return addresses when subroutines are called. In the old days the stack allowd 12 levels of nesting, in modern implementations this is not the case.

### Timers

1. Delay timer
2. Sound timer

### Keypad



### Fetch/decode/execute

TODO

### Opcode table

| Opcode       | Instruction   |
| ------------ | ------------- |
| 00E0         | Clear screen  |

