# 40 rows

import helpers


def get_new_line(line):
    traps = [("^", "^", "."), (".", "^", "^"), ("^", ".", "."), (".", ".", "^")]

    data = list(line)
    data.insert(0, ".")
    data.append(".")

    result = list()
    for (x, y, z) in zip(data, data[1:], data[2:]):
        token = "^" if (x, y, z) in traps else "."
        result.append(token)

    return "".join(result)


def get_safe_tiles(data, depth):
    safe_tiles = 0
    for _ in range(depth):
        safe_tiles += data.count(".")
        data = get_new_line(data)
    return safe_tiles


if __name__ == "__main__":
    lines = helpers.get_lines(r"../data/day_18.txt")
    line = lines[0]

    # line = "..^^."
    # line = ".^^.^.^^^^"

    part_01 = get_safe_tiles(line, 40)
    assert part_01 == 2035

    part_02 = get_safe_tiles(line, 400000)
    assert part_02 == 20000577
