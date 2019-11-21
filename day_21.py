import helpers
from collections import deque


def hash_text(puzzle_start, lines):

    for line in lines:

        cmd, *args = line.split()

        if cmd == "reverse":
            start, end = int(args[1]), int(args[3])
            # print(f"reverse({start}, {end}, {puzzle_start})")
            part1 = puzzle_start[start : end + 1]
            part1 = part1[::-1]
            puzzle_start = puzzle_start[:start] + part1 + puzzle_start[end + 1 :]

        elif cmd == "rotate":
            instruction = args[0]
            rotate = deque(list(puzzle_start))

            if instruction == "based":
                index = puzzle_start.index(args[-1])

                count = 1 + index + int(index >= 4)
                # print(index, args[-1], count, puzzle_start)
                rotate.rotate(count)

            else:
                r = int(args[1])
                r = r if args[0] == "right" else r * -1
                rotate.rotate(r)

            puzzle_start = "".join(rotate)

        elif cmd == "swap":
            index1, index2 = -1, -1
            if "position" in args:
                index1, index2 = int(args[1]), int(args[4])

            elif "letter" in args:
                a, b = args[1], args[4]
                index1 = puzzle_start.index(a)
                index2 = puzzle_start.index(b)

            p = list(puzzle_start)
            p[index1], p[index2] = p[index2], p[index1]
            puzzle_start = "".join(p)

        elif cmd == "move":
            index1, index2 = int(args[1]), int(args[4])
            items = list(puzzle_start)

            c = items[index1]
            items.remove(c)
            items.insert(index2, c)
            puzzle_start = "".join(items)

    return puzzle_start


if __name__ == "__main__":
    # puzzle_start = "abcde"
    # lines = helpers.get_lines(r"./data/day_21_test.txt")
    # r = hash_text(puzzle_start, lines)
    # print(r)

    puzzle_start = "abcdefgh"
    lines = helpers.get_lines(r"./data/day_21.txt")
    r = hash_text(puzzle_start, lines)
    print("Part01:", r)

    # Not yet done
    puzzle_start = "fbgdceah"
    r = hash_text(puzzle_start, reversed(lines))
    print("Part02:", r)
