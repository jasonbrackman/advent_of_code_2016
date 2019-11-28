import helpers


class Machine:
    def __init__(self, data, a=None):
        self.registers = {"a": 0, "b": 0, "c": 0, "d": 0}
        self.toggle_cache = dict()
        self.pointer: int = 0

        if a is not None:
            self.registers["a"] = a

        self.instructions = self.prep_instructions(data)

        while self.pointer < len(self.instructions):
            self.op_code()

    @staticmethod
    def prep_instructions(data):
        instructions = []
        lines = helpers.get_lines(data)
        for line in lines:
            op, *args = line.split()
            instructions.append((op, args))
        return instructions

    def op_code(self):
        op, args = self.instructions[self.pointer]

        pointer_jump = 1

        if op == "tgl":
            # don't worry about items that are beyond the program bounds
            # - if this occurs nothing happens
            arg1 = self.pointer + self.get_value(args[0])
            if 0 <= arg1 < len(self.instructions):
                # Get future instruction
                op, args = self.instructions[arg1]

                if len(args) == 1:
                    op = "dec" if op == "inc" else "inc"
                if len(args) == 2:
                    op = "cpy" if op == "jnz" else "jnz"

                self.instructions[arg1] = (op, args)
            else:
                print(
                    f"skipping a toggle out of bounds: {arg1} / {len(self.instructions)-1}"
                )

            for index, items in enumerate(self.instructions):
                op_code = items[0]
                args = []
                for i in range(len(items[1])):
                    args.append(str(self.get_value(items[1][i])))
                print(f"{index:02}: {items[0]} {str(items[1]):<15} | {op_code}({','.join(args)})")
            print(f"{self.registers}")

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

"""
0 cpy a b
1 dec b
2 cpy a d
3 cpy 0 a
4 cpy b c
5 inc a
6 dec c
7 jnz c -2
8 dec d
9 jnz d -5
10 dec b
11 cpy b c
12 cpy c d
13 dec d
14 inc c
15 jnz d -2
16 tgl c
17 cpy -16 c
18 jnz 1 c
19 cpy 73 c
20 jnz 91 d
21 inc a
22 inc d
23 jnz d -2
24 inc c
25 jnz c -5
dict_items([(24, ('dec', ['c'])), (22, ('dec', ['d'])), (20, ('cpy', ['91', 'd']))])
{'a': 239500800, 'b': 2, 'c': 4, 'd': 0}

dict_items(
    [
    (24, ('dec', ['c'])), 
    (22, ('dec', ['d'])), 
    (20, ('cpy', ['91', 'd'])),
    (18, ('cpy', ['1', 'c']))
    ])

{'a': 479001600, 'b': 0, 'c': 2, 'd': 0}

132
1320
11880
95040
665280
3991680
19958400
79833600
239500800
479001600‬"""