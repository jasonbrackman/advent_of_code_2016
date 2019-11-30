import helpers


class Machine:
    def __init__(self, data, a=None, record_telemetry=False, hack=False):

        self.registers = {"a": 0, "b": 0, "c": 0, "d": 0}
        self.toggle_cache = dict()
        self.pointer: int = 0

        if a is not None:
            self.registers["a"] = a

        self.instructions = self.prep_instructions(data)

        self.hack = hack
        self.record_telemetry = record_telemetry
        if self.record_telemetry:
            # Required to find out which lines were getting hit a lot
            # stuck to the lines before toggle for optimization since after would change.
            self.telemetry = {x: 0 for x in range(len(self.instructions))}

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
        if self.record_telemetry:
            self.telemetry[self.pointer] += 1

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
            # self.pprint_debug()
        elif op == "cpy":
            # Copies arg1 (reg/value) to register in arg2
            arg1, arg2 = args
            arg1 = self.get_value(arg1)
            self.registers[arg2] = arg1

        elif op == "inc":
            if self.hack and self.pointer == 5:
                # a, c, d
                # a * c * (d * b)
                # c must get to zero
                # d must get to zero
                result = (self.registers["a"] + self.registers["c"]) * (
                    self.registers["d"]
                )
                self.registers["a"] = result
                self.registers["c"] = 1
                self.registers["d"] = 1

            else:
                # Increases arg1 register by one
                self.registers[args[0]] += 1

        elif op == "dec":
            #     self.registers['d'] = 0
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

    def pprint_debug(self):
        for index, items in enumerate(self.instructions):
            op_code = items[0]
            args = []
            for i in range(len(items[1])):
                args.append(str(self.get_value(items[1][i])))

            icon = "<==" if index == self.pointer else ""
            comments = {
                5: "'a' + r'c'-1 * 'd' and then leave one at c",
                8: "'d' * 'b'-1",
                13: "'c' + 'd', d = 0",
            }
            comment = comments.get(index, "")
            icon = icon + "" + comment

            print(
                f"{index:02}: {items[0]} {str(items[1]):<15} | {op_code}({','.join(args)}) {icon}"
            )
        print(f"{self.registers}")

    def get_value(self, arg):
        value = self.registers.get(arg, None)
        if value is not None:
            return value
        return int(arg)


if __name__ == "__main__":
    import time

    data_test = r"./data/day_23_test.txt"
    puzzle_path = r"./data/day_23.txt"

    test = Machine(data_test)
    assert test.registers["a"] == 3

    t1 = time.perf_counter()
    part1 = Machine(puzzle_path, a=7, record_telemetry=False, hack=True)
    assert part1.registers["a"] == 11683
    print("Part01:", part1.registers["a"])

    # print("Telemetry:", part1.telemetry)

    part2 = Machine(puzzle_path, a=12, hack=True)
    assert part2.registers["a"] == 479008243
    print("Part02:", part2.registers["a"])

    print(f"Completed Day 23: {time.perf_counter() - t1}")
