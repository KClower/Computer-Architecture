"""CPU functionality."""

import sys



LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
ADD = 0b10100000
SUB = 0b10100001
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.registers = [0] * 8
        self.SP = 7
        self.registers[self.SP] = 0xF4       
        self.ram = [0] * 256
        self.pc = 0


    def load(self):
        """Load a program into memory."""

        address = 0

        if len(sys.argv) != 2:
            print("Not Valid")
            sys.exit(1)

        # For now, we've just hardcoded a program:
        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8  (op code 130)
        #     0b00000000, #           (reg 0)
        #     0b00001000, #           (value 8)
        #     0b01000111, # PRN R0    (op code 71)
        #     0b00000000, #           (reg 0)
        #     0b00000001, # HLT       (value 1)
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

        with open(sys.argv[1]) as f:
            for line in f:
                line = line.strip()

                if line == "" or line[0] == "#":
                    continue

                try:
                    str_value = line.split("#")[0]
                    value = int(str_value, 2)
                except ValueError:
                    print(f"Invalid Number: {str_value}")
                    sys.exit(2)
                
                self.ram[address] = value
                address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == ADD:
            self.registers[reg_a] += self.registers[reg_b]
        elif op == SUB: 
            self.registers[reg_a] -= self.registers[reg_b]
        elif op == MUL:
            self.registers[reg_a] *= self.registers[reg_b]
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



    def ram_read(self, address):
        return self.ram[address]
        


    def ram_write(self, value, address):
        self.ram[address] = value
        


    def run(self):
        """Run the CPU."""
        

        while True:
            op = self.ram_read(self.pc)

            if op == LDI:
                register_num = self.ram_read(self.pc + 1)
                register_value = self.ram_read(self.pc + 2)
                self.registers[register_num] = register_value

            elif op == ADD:
                reg_a = self.ram_read(self.pc + 1)
                reg_b = self.ram_read(self.pc + 2)
                self.alu(ADD, reg_a, reg_b)

            elif op == SUB:
                reg_a = self.ram_read(self.pc + 1)
                reg_b = self.ram_read(self.pc + 2)
                self.alu(SUB, reg_a, reg_b)

            elif op == MUL:
                reg_a = self.ram_read(self.pc + 1)
                reg_b = self.ram_read(self.pc + 2)
                self.alu(MUL, reg_a, reg_b)
                
            elif op == PRN:
                register_num = self.ram_read(self.pc + 1)
                print(self.registers[register_num])

            elif op == PUSH:
                self.registers[self.SP] -= 1
                register_num = self.ram_read(self.pc + 1)                            
                self.ram_write(self.registers[register_num], self.registers[self.SP])

                print(self.ram[0xf0:0xf4])

            elif op == POP:
                register_num = self.ram_read(self.pc + 1)
                self.registers[register_num] = self.ram_read(self.registers[self.SP])              
                self.registers[self.SP] += 1

            elif op == CALL:
                register_num = self.ram_read(self.pc + 1)
                return_address = self.pc + 2
                self.registers[self.SP] -= 1
                self.ram_write(return_address, self.registers[self.SP])
                self.pc = self.registers[register_num]
                continue

            elif op == RET:
                self.pc = self.ram_read(self.registers[self.SP])
                self.registers[self.SP] += 1
                continue

            elif op == HLT:
                sys.exit(1)

            else:
                print(f"Unknown instruction {op} at address {self.pc}")
                sys.exit(1)

            op_len = ((op & 0b11000000) >> 6) +1
            self.pc += op_len

