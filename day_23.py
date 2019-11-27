import helpers


class Machine:
    def __init__(self, data, a=None):
        self.registers = {"a": 0, "b": 0, "c": 0, "d": 0}
        self.toggle_cache = dict()
        self.pointer: int = 0

        if a is not None:
            self.registers["a"] = a

        self.instructions = helpers.get_lines(data)

        while self.pointer < len(self.instructions):
            self.op_code(self.instructions[self.pointer])

    def op_code(self, instruction):
        op, *args = instruction.split()

        if self.toggle_cache.get(self.pointer, None) is not None:
            op, args = self.toggle_cache[self.pointer]
            # self.toggle_cache[self.pointer] = None

        pointer_jump = 1

        if op == "tgl":
            # don't worry about items that are beyond the program bounds
            # - if this occurs nothing happens
            arg1 = self.pointer + self.get_value(args[0])
            if 0 <= arg1 < len(self.instructions):

                future_instruction = self.instructions[arg1]

                op, *args = future_instruction.split()
                if len(args) == 1:
                    op = "dec" if op == "inc" else "inc"
                if len(args) == 2:
                    op = "cpy" if op == "jnz" else "jnz"

                self.toggle_cache[arg1] = op, args
            else:
                print(
                    f"skipping a toggle out of bounds: {arg1} / {len(self.instructions)-1}"
                )

        elif op == "cpy":
            # Copies arg1 (reg/value) to register in arg2
            arg1, arg2 = args
            arg1 = self.get_value(arg1)
            self.registers[arg2] = arg1

        elif op == "inc":
            # Increases arg1 register by one
            self.registers[args[0]] += 1

        elif op == "dec":
            # Decreases arg1 register by one
            self.registers[args[0]] -= 1

        elif op == "jnz":
            # jumps to an instruction y away (positive means forward; negative means backward),
            # but only if x is not zero
            arg1, arg2 = args
            arg1 = self.get_value(arg1)
            arg2 = self.get_value(arg2)

            if arg1 != 0:
                pointer_jump = arg2

        else:
            raise ValueError(f"Unknown opcode: {op}")

        # print(self.pointer, self.registers, self.toggle_cache)

        self.pointer += pointer_jump

    def get_value(self, arg):
        value = self.registers.get(arg, None)
        if value is not None:
            return value
        return int(arg)


if __name__ == "__main__":

    data_test = r"./data/day_23_test.txt"
    test = Machine(data_test)
    assert test.registers["a"] == 3

    puzzle_path = r"./data/day_23.txt"
    part1 = Machine(puzzle_path, a=7)
    assert part1.registers["a"] == 11683

    part2 = Machine(puzzle_path, a=12)
    print(part2.registers["a"])
