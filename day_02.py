import helpers

directions = {"R": (0, 1), "L": (0, -1), "U": (-1, 0), "D": (1, 0)}

pad_01 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

pad_02 = [
    [0, 0, 1, 0, 0],
    [0, 2, 3, 4, 0],
    [5, 6, 7, 8, 9],
    [0, "A", "B", "C", 0],
    [0, 0, "D", 0, 0],
]


def convert_to_positions(line):
    instructions = [directions[c] for c in line]
    return instructions


def parse_lines():
    lines = helpers.get_lines(r"./data/day_02.txt")
    return [convert_to_positions(line) for line in lines]


def add_positions(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2

    return x1 + x2, y1 + y2


def solve(instructions, pad, current):
    code = []
    for instruction in instructions:
        for (x, y) in instruction:
            (x_test, y_test) = add_positions(current, (x, y))
            if 0 <= x_test < len(pad[0]) and 0 <= y_test < len(pad[0]):
                if pad[x_test][y_test] != 0:
                    current = (x_test, y_test)

        # Whatever the last number is added
        code.append(pad[current[0]][current[1]])
    return code


def test_parts():
    instructions = [
        convert_to_positions(line) for line in ["ULL", "RRDDD", "LURDL", "UUUUD"]
    ]
    result = solve(instructions, pad_01, current=(1, 1))
    assert result == [1, 9, 8, 5]

    result = solve(instructions, pad_02, current=(2, 0))
    assert result == [5, "D", "B", 3]


def part_01(instructions):
    result = "".join(str(i) for i in solve(instructions, pad_01, current=(1, 1)))
    return result


def part_02(instructions):
    result = "".join(str(i) for i in solve(instructions, pad_02, current=(2, 0)))
    return result


if __name__ == "__main__":
    test_parts()

    info = parse_lines()
    assert part_01(info) == "92435"
    assert part_02(info) == "C1A88"
