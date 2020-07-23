"""CPU functionality."""

import sys

''' Opcodes ''' 

# halt the cpu and exit the emulator
HLT = 0b00000001 

# load 'immediate', store a value in register
LDI = 0b10000010 

# prints the numeric value stored in a register
PRN = 0b01000111 

ADD = 0b10100000
SUB = 0b10100001
MUL = 0b10100010
DIV = 0b10100011

AND  = 0b10101000
OR   = 0b10101010
XOR  = 0b10101011
NOT  = 0b01101001

SHL  = 0b10101100
SHR  = 0b10101101

INC  = 0b01100101
DEC  = 0b01100110
CMP  = 0b10100111



class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # Add list properties to the CPU class to hold 256 
        # bytes of memory and 8 general purpose registers
        
        self.ram = [0b00000000] * 256
        self.reg = [0b00000000] * 8
        self.PC = 0
        self.flag = 0b00000000
        self.branch_table = {
            LDI: self.ldi,
            PRN: self.prn,
            HLT: self.hlt,
            MUL: self.alu,
            ADD: self.alu,
            DIV: self.alu,
            SUB: self.alu,
            AND: self.alu,
            OR: self.alu,
            XOR: self.alu,
            NOT: self.alu,
            SHL: self.alu,
            SHR: self.alu,
            INC: self.alu,
            DEC: self.alu,
            CMP: self.alu
        }
    def ldi(self, op_a, op_b):
        self.reg[op_a] = op_b 
    
    def prn(self, op_a, op_b):
        print(self.reg[op_a])
    
    def hlt(self, op_a, op_b):
        sys.exit()
        
    # add ram methods - read() and write() - that access the
    # RAM inside the CPU object
    def ram_read(self, address):
        return self.ram[address]
    
    def ram_write(self, value, address):
        self.ram[address] = value

    def load(self, filename):
        """Load a program into memory."""

        address = 0

        with open(filename) as f: 
            for line in f:
                line = line.split('#')
                try:
                    instruction = int(line[0], 2)
                except ValueError:
                    continue
                self.ram[address] = instruction
                address += 1
        '''
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
        '''

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == ADD:
            self.reg[reg_a] += self.reg[reg_b]
        elif op == SUB:
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == MUL:
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == DIV:
            self.reg[reg_a] //= self.reg[reg_b]
        elif op == AND:
            self.reg[reg_a] &= self.reg[reg_b]
        elif op == OR:
            self.reg[reg_a] |= self.reg[reg_b]
        elif op == XOR:
            self.reg[reg_a] ^= self.reg[reg_b]
        elif op == NOT:
            self.reg[reg_a] = ~self.reg[reg_a]
        elif op == SHL:
            self.reg[reg_a] = self.reg[reg_a] << reg_b
        elif op == SHR:
            self.reg[reg_a] = self.reg[reg_a] >> reg_b
        elif op == INC:
            self.reg[reg_a] += 1
        elif op == DEC:
            self.reg[reg_a] -= 1
        elif op == CMP:
            self.flag = ((self.reg[reg_a] < self.reg[reg_b]) << 2) | \
                        ((self.reg[reg_a] > self.reg[reg_b]) << 1) | \
                        ((self.reg[reg_a] == self.reg[reg_b]) << 0)
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

        while running:
            ir = self.ram_read(self.PC)
            op_a = self.ram_read(self.PC + 1)
            op_b = self.ram_read(self.PC + 2)

            # >> bitwise shift right by 'x' places
            # new bits on the right hand side are zeroes
            num_operands = ir >> 6

            ALU_operation = (ir >> 5) & 1

            if ir in self.branch_table:
                if ALU_operation:
                    self.branch_table[ir](ir, op_a, op_b)
                else:
                    self.brach_table[ir](op_a, op_b)
            else:
                print('Unsupported Op')
            
            self.PC += num_operands + 1 # +1 for opcode

            '''
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
            '''