import helpers


class Machine:
    registers = {"a": 0, "b": 0, "c": 0, "d": 0}

    pointer: int = 0

    def __init__(self, data, c: 0):
        self.registers["c"] = c
        self.instructions = helpers.get_lines(data)

        while self.pointer < len(self.instructions):
            self.op_code(self.instructions[self.pointer])

    def op_code(self, instruction):
        op, *args = instruction.split()
        pointer_jump = 1
        if op == "cpy":
            # Copies arg1 (reg/value) to register in arg2
            arg1, arg2 = args
            arg1 = self.get_value(arg1)
            self.registers[arg2] = arg1

        if op == "inc":
            # Increases arg1 register by one
            self.registers[args[0]] += 1

        if op == "dec":
            # Decreases arg1 register by one
            self.registers[args[0]] -= 1

        if op == "jnz":
            # jumps to an instruction y away (positive means forward; negative means backward),
            # but only if x is not zero
            arg1, arg2 = args
            arg1 = self.get_value(arg1)
            arg2 = self.get_value(arg2)

            if arg1 != 0:
                pointer_jump = arg2

        self.pointer += pointer_jump

    def get_value(self, arg):
        value = self.registers.get(arg, None)
        if value is not None:
            return value
        return int(arg)


if __name__ == "__main__":
    data_part1 = r"./data/day_12.txt"
    data_test = r"./data/day_12_test.txt"

    m1 = Machine(data_part1, c=0)
    assert m1.registers["a"] == 317993

    m2 = Machine(data_part1, c=1)
    assert m2.registers["a"] == 9227647
