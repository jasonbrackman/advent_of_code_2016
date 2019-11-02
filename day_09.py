import helpers
import re

pattern = re.compile(r"(\w+)|\((\d+)x(\d+)\)")


def yield_instructions(lines):
    for line in lines:
        is_marker = False
        instructions = (0, 0)
        string_builder = ""
        for it in pattern.finditer(line):
            a, b, c = it.groups()
            if a is None:
                if is_marker:
                    string_builder += f"({b}x{c})"
                else:
                    instructions = int(b), int(c)
                    is_marker = True
            else:
                string_builder += a

            if len(string_builder) >= instructions[0]:
                new_str = (
                    string_builder[: instructions[0]] * instructions[1]
                ) + string_builder[instructions[0] :]
                yield new_str
                is_marker = False
                string_builder = ""


def main():
    lines = helpers.get_lines(r"./data/day_09.txt")

    part_01 = ""
    for itm in yield_instructions(lines):
        part_01 += itm
    assert len(part_01) == 183269


if __name__ == "__main__":
    main()
