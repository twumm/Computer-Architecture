"""CPU functionality."""

import sys

# operation codes
HLT = 0b00000001
PRN = 0b01000111
LDI = 0b10000010

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.halted = False

    def load(self):
        """Load a program into memory."""

        address = 0
        programs = []
        try:
            filename = sys.argv[1]
        except:
            print('Please add an ls8 file path')

        with open(filename) as f:
            for line in f:
                line = line.split('#')[0]
                line = line.strip()

                if line == '':
                    continue

                # val = int(line)
                print(line)
                programs.append(int(line, 2))
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
        print(programs)
        for instruction in programs:
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
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()
    
    def ram_read(self, read_address):
        """Accept the address to read and return the value stored there"""
        return self.ram[read_address]

    def ram_write(self, value, write_address):
        self.ram.insert(write_address, value)

    def run(self):
        """Run the CPU."""
        inc_size = 0
        while not self.halted:
            cmd = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if cmd == HLT:
                self.halted = True
                sys.exit(-1)

            elif cmd == PRN:
                reg_index = operand_a
                num = self.reg[reg_index]
                print(num)
                inc_size = 2
            
            elif cmd == LDI:
                self.reg[operand_a] = operand_b
                inc_size = 3
            
            self.pc += inc_size 

small_cpu = CPU()
small_cpu.load()