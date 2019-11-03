import helpers
import re

pattern = re.compile(r"\((\d+)x(\d+)\)")


def process_instructions(line):
    needle = pattern.search(line)

    if not needle:
        return len(line)

    pos = needle.start(0)
    index = int(needle.group(1))
    count = int(needle.group(2))
    i = pos + len(needle.group(0))

    return (
        len(line[:pos])
        + process_instructions(line[i : i + index]) * count
        + process_instructions(line[i + index :])
    )


def process_instructions_01(line):
    needle = pattern.search(line)
    if not needle:
        return len(line)

    pos: int = needle.start(0)
    index: int = int(needle.group(1))
    count: int = int(needle.group(2))
    i: int = pos + len(needle.group(0))

    new_line = line[i : i + index] * count

    return len(line[:pos]) + len(new_line) + process_instructions_01(line[i + index :])


def main():
    lines = helpers.get_lines(r"./data/day_09.txt")

    part_01 = process_instructions_01(lines[0])
    assert part_01 == 183269

    # lines = ["(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN"]
    part_02 = process_instructions(lines[0])
    assert part_02 == 11317278863


if __name__ == "__main__":
    main()
