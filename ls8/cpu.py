"""CPU functionality."""

import sys

''' Opcodes - Command Variables''' 

# halt the cpu and exit the emulator
HLT = 0b00000001 

# load 'immediate', store a value in register
LDI = 0b10000010 

# prints the numeric value stored in a register
PRN = 0b01000111 

POP = 0b01000110
PUSH = 0b01000101
CALL = 0b01010000
RET = 0b00010001

ADD = 0b10100000
SUB = 0b10100001
MUL = 0b10100010
DIV = 0b10100011
MOD = 0b10100100

INC = 0b01100101
DEC = 0b01100110

CMP = 0b10100111

AND = 0b10101000
NOT = 0b01101001
OR = 0b10101010
XOR = 0b10101011
SHL = 0b10101100
SHR = 0b10101101

SP = 7

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # Add list properties to the CPU class to hold 256 
        # bytes of memory and 8 general purpose registers
        
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.reg[SP] = 0xF4
        
        self.PC = 0
        self.FL = 0

        self.branch_table = {
            HLT: self.hlt,
            LDI: self.ldi,
            PRN: self.prn,
            POP: self.pop,
            PUSH: self.push,
            CALL: self.call, 
            RET: self.ret, 

            ADD: self.alu,
            SUB: self.alu,
            MUL: self.alu,
            DIV: self.alu,
            MOD: self.alu,

            INC: self.alu,
            DEC: self.alu,

            CMP: self.alu,

            AND: self.alu,
            NOT: self.alu,
            OR: self.alu,
            XOR: self.alu,
            SHL: self.alu,
            SHR: self.alu
        }

    def ldi(self, op_a, op_b):
        ''' sets a specific register to a specific value '''
        self.reg[op_a] = op_b 
    
    def prn(self, op_a, op_b=None):
        ''' prints a specific value '''
        print(self.reg[op_a])

    def hlt(self, op_a=None, op_b=None):
        ''' halts the CPU and exits the emulator '''
        sys.exit()

    def pop(self, op_a, op_b=None):
        ''' removes values from stack using arithmetic logic unit (ALU) '''
        self.reg[op_a] = self.ram_read(self.reg[SP])
        self.reg[SP] += 1

    def push(self, op_a, op_b=None):
        ''' adds values to stack using arithmetic logic unit (ALU) ''' 
        self.reg[SP] -= 1
        self.ram_write(self.reg[SP], self.reg[op_a])

    def call(self, op_a, op_b=None):
        ''' jumps to address ''' 
        # push on the stack
        self.reg[SP] -= 1
        self.ram_write(self.reg[SP], self.PC + 2)
        # set the program counter (PC) to the value in the given register
        self.PC = self.reg[op_a]
    
    def ret(self, op_a=None, op_b=None):
        ''' returns back to where it was called from '''
        # pop return address from top of stack
        # set the program counter (PC)
        self.PC = self.ram_read(self.reg[SP])
        self.reg[SP] += 1

    def ram_read(self, address):
        ''' reads the CPU object in RAM ''' 
        return self.ram[address]
    
    def ram_write(self, address, value):
        ''' writes the CPU object in RAM '''
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
            self.reg[reg_a] /= self.reg[reg_b]
        elif op == MOD:
            self.reg[reg_a] %= self.reg[reg_b]
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
            self.FL = ((self.reg[reg_a] < self.reg[reg_b]) << 2) | \
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

            PC_set = (ir >> 4) & 1

            ALU_operation = (ir >> 5) & 1

            if ir in self.branch_table:
                if ALU_operation:
                    self.branch_table[ir](ir, op_a, op_b)
                else:
                    self.branch_table[ir](op_a, op_b)
            else:
                print('Unsupported operation')

            if not PC_set:
                self.PC += num_operands + 1 # +1 for opcode