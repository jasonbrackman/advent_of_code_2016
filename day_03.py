import helpers
import re


def parse_lines():
    lines = helpers.get_lines("./data/day_03.txt")
    pattern = re.compile(r"(\d+)\s+(\d+)\s+(\d+)")
    results = list()
    for line in lines:
        found = pattern.search(line)
        a, b, c = found.groups()
        results.append((int(a), int(b), int(c)))

    return results


def is_triangle_valid(items):
    a, b, c = items
    return a + c > b and a + b > c and c + b > a


def part_01():
    values = parse_lines()
    count = 0
    for value in values:
        if is_triangle_valid(value):
            count += 1

    return count


def part_02():
    values = parse_lines()

    count = 0
    for seta, setb, setc in zip(*[iter(values)] * 3):
        # Transpose the 3 x 3 numbers
        x1, y1, z1 = seta
        x2, y2, z2 = setb
        x3, y3, z3 = setc
        for value in ((x1, x2, x3), (y1, y2, y3), (z1, z2, z3)):

            if is_triangle_valid(value):
                count += 1

    return count


def is_valid_triangle(value):
    result = True

    a = int(value[0])
    b = int(value[1])
    c = int(value[2])

    if a + b > c:
        result = False
    if a + c > b:
        result = False
    if b + c > a:
        result = False

    return result


if __name__ == "__main__":
    assert part_01() == 1032
    assert part_02() == 1838
