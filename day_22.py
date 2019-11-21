import helpers
import re
from itertools import permutations

needle = re.compile(r".*x(\d+)-y(\d+)")


class Node:
    def __init__(self, name, used, avail):
        self.name = name
        self.used = used
        self.avail = avail

    def __hash__(self):
        return hash(self.name) + hash(self.used) + hash(self.avail)

    def is_valid_pair(self, other) -> bool:
        if self.used == 0:
            return False

        if hash(self) == hash(other):
            return False

        if self.used > other.avail:
            return False

        return True


def get_data_from_lines():
    lines = helpers.get_lines(r"./data/day_22.txt")
    i_lines = iter(lines)

    # skip command line
    next(i_lines)

    # skip header
    next(i_lines).split()

    data = []
    for line in i_lines:
        point, size, used, avail, percentage = line.split()
        row, col = needle.search(point).groups()
        row, col = int(row), int(col)
        if len(data) == row:
            data.append([])
        new_node = Node(point, int(used[:-1]), int(avail[:-1]))
        data[row].append(new_node)

    return data


def part_01():
    data = get_data_from_lines()

    nodes = list()
    for row in data:
        for col in row:
            nodes.append(col)

    count = 0
    for (a, b) in permutations(nodes, 2):
        if a.is_valid_pair(b):
            count += 1

    return count


if __name__ == "__main__":
    result = part_01()
    print("Part01:", result)
