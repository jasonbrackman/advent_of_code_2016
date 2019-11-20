from itertools import cycle
from collections import deque


class Elves:
    def __init__(self, puzzle_input):
        self.values = [1] * puzzle_input
        self.bad = []
        self.length = len(self.values)

    def get_next_elf(self, from_index: int):
        while True:
            if self.values[from_index] > 0:
                return from_index, self.values[from_index]
            from_index = (from_index + 1) % self.length

    def get_half_way_elf(self, from_key):
        half_way = (self.length - len(self.bad)) // 2
        print("Half:", half_way)
        key = (from_key + half_way) % self.length
        print("Key:", key)


        count = 0

        for index, value in enumerate(cycle(self.values)):
            new_index = index % self.length
            if self.values[new_index] == 0:
                count += 1

            if index - count == key:
                final_index = new_index-count % self.length
                return final_index, self.values[final_index]


def steal_from_right(puzzle_input):
    elves = Elves(puzzle_input)
    count = 0
    while True:
        fk, fv = elves.get_next_elf(count)
        sk, sv = elves.get_next_elf((fk + 1) % elves.length)
        if (fk, fv) == (sk, sv):
            return fk + 1

        else:
            elves.values[fk] += sv
            elves.values[sk] = 0
            count = (sk + 1) % elves.length


def steal_from_half_way_across(puzzle_input):
    elves = Elves(puzzle_input)

    count = 0
    while True:
        fk, fv = elves.get_next_elf(count)
        sk, sv = elves.get_half_way_elf(fk)
        print(fk+1, sk+1, elves.values)
        if (fk, fv) == (sk, sv):
            return fk + 1

        else:
            elves.values[fk] += sv
            elves.values[sk] = 0
            elves.bad.append(sk)
        # print(fk, sk, elves.values)
        count = (fk+1) % elves.length


def part_01():
    puzzle_input = 3017957
    part_01 = steal_from_right(puzzle_input)
    assert part_01 == 1841611


def josephus_winner(n):
    """https://www.youtube.com/watch?v=uCsD3ZGzMgE"""
    true_power_of_two = 1
    while True:
        if true_power_of_two < n:
            true_power_of_two *= 2
        if true_power_of_two > n:
            true_power_of_two /= 2
            break

    left_over = n - true_power_of_two
    return left_over * 2 + 1


def faster_part_01():
    puzzle_input = 3017957
    result = josephus_winner(puzzle_input)
    assert int(result) == 1841611


def part_02():
    # part_02
    # -- ugg quite the mess here ... lots of help from wikipedia and AOC on reddit for this one...
    puzzle = deque([x for x in range(1, 3017957 + 1)])
    puzzle_length = len(puzzle)
    current_position = 0
    while puzzle_length != 1:
        index = (puzzle_length // 2) - current_position
        # print(index, current_position, puzzle)
        puzzle.rotate(-index)
        puzzle.popleft()
        puzzle_length -= 1
        current_position = (current_position + index - 1) % puzzle_length
    assert puzzle[0] == 1423634


if __name__ == "__main__":
    faster_part_01()
    part_02()



