"""CPU functionality."""

import sys

HLT = 1
LDI = 130
PRN = 71
MUL = 162


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.pc = 0  # Program Counter

    def load(self):
        """Load a program into memory."""
        progname = sys.argv[1]
        address = 0

        with open(progname) as f:
            # iterate through each line in the program
            for line in f:
                # remove any comments
                line = line.split("#")[0]
                # remove whitespace
                line = line.strip()
                # skip empty lines
                if line == "":
                    continue

                value = int(line, 2)
                # set the instruction to memory
                self.ram[address] = value
                address += 1

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        # MAR = Memory Address Register, contains the address that is being read or written to
        # MDR =  Memory Data Register, contains the data that was read or the data to write
        self.ram[MAR] = MDR

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        # load the program
        self.load()

        while True:
            # Instruction Register, contains a copy of the currently executing instruction
            IR = self.ram[self.pc]
            # Grab AA of the program instruction for the operand count
            operand_count = IR >> 6

            if IR == LDI:
                address = self.ram[self.pc + 1]
                value = self.ram[self.pc + 2]
                # store the data
                self.reg[address] = value
                # increment the PC by 3 to skip the arguments
            elif IR == PRN:
                data = self.ram[self.pc + 1]
                # print the data
                print(self.reg[data])
                # increment the PC by 2 to skip the argument
            elif IR == MUL:
                reg_a = self.ram[self.pc + 1]
                reg_b = self.ram[self.pc + 2]

                self.reg[reg_a] *= self.reg[reg_b]
            elif IR == HLT:
                sys.exit(0)
            else:
                print(f"I did not understand that command: {IR}")
                sys.exit(1)
            self.pc += operand_count + 1
