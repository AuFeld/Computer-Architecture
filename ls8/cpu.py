"""CPU functionality."""

import sys

''' Operands ''' 

# halt the cpu and exit the emulator
HLT = 0b00000001 

# load 'immediate', store a value in register
LDI = 0b10000010 

# prints the numeric value stored in a register
PRN = 0b01000111 


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # Add list properties to the CPU class to hold 256 
        # bytes of memory and 8 general purpose registers
        
        self.ram = [0b00000000] * 256
        self.reg = [0b00000000] * 8
        self.PC = 0

    # add ram methods - read() and write() - that access the
    # RAM inside the CPU object
    def ram_read(self, address):
        return self.ram[address]
    
    def ram_write(self, value, address):
        self.ram[address] = value

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.PC,
            #self.fl,
            #self.ie,
            self.ram_read(self.PC),
            self.ram_read(self.PC + 1),
            self.ram_read(self.PC + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        ''' implement the core of the cpu's run() mentod
        reads the memory address that's stored in the
        register PC, and store the result in IR (instrction
        register) '''
        # set running to true
        running = True

        self.IR = self.ram_read(self.PC)
        operand_a = self.ram_read(self.PC + 1)
        operand_b = self.ram_read(self.PC + 2)

        while running:
            # add the LDI instruction
            # set value of register to an integer
            if self.IR == LDI:
                self.reg[operand_a] = operand_b
                self.PC += 3
            # add PRN instruction
            # print numeric value stored in given register
            elif self.IR == PRN:
                print(self.reg[operand_a])
                self.PC += 2
            # implement the HLT instruction handler.
            # halt the CPU and exit the emulator
            elif self.IR == HLT:
                running = False
                self.PC += 1
            
        else:
            print(f'Unknown instruction {self.IR} at address {self.PC}')
            sys.exit(1)

        self.IR = self.ram_read(self.PC)
        operand_a = self.ram_read(self.PC + 1)
        operand_b = self.ram_read(self.PC + 2)
