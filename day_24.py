from itertools import permutations

from helpers import astar, get_lines


class Maze:
    def __init__(self, puzzle, start=None, goal=None):
        self.puzzle = [list(line) for line in list(puzzle)]

        self.start = start
        self.goal_pos = goal

    def __str__(self):
        buffer = ""
        for row in self.puzzle:
            for col in row:
                buffer += col
            buffer += "\n"
        return buffer

    def __hash__(self):
        return hash((str(self.puzzle), self.start, self.goal_pos))

    def heuristic(self):
        # Manhattan Distance
        x1, y1 = self.start
        x2, y2 = self.goal_pos
        x_dist: int = abs(x1 - (x2 - 1))
        y_dist: int = abs(y1 - y2)

        return x_dist + y_dist

    @staticmethod
    def find_numbers(data):
        items = dict()
        for r, row in enumerate(data):
            for c, col in enumerate(row):
                if col.isdigit():
                    items[int(col)] = (r, c)
        return items

    def goal(self):
        return self.goal_pos == self.start

    def neighbours(self):
        dirs = [(-1, 0), (+1, 0), (0, -1), (0, +1)]

        sucs = list()
        for d in dirs:
            new_row = d[0] + self.start[0]
            new_col = d[1] + self.start[1]
            new_start = (new_row, new_col)

            if 0 <= new_row <= len(self.puzzle) and 0 <= new_col <= len(self.puzzle[0]):
                icon = self.puzzle[new_row][new_col]
                if icon != "#":
                    np = self.puzzle[:]
                    np[new_row][new_col] = np[self.start[0]][self.start[1]]
                    np[self.start[0]][self.start[1]], np[new_row][new_col] = (
                        np[new_row][new_col],
                        ".",
                    )
                    sucs.append(Maze(np, start=new_start, goal=self.goal_pos))

        return sucs


def travelling_elves(info_data, back_to_start=False):
    numbers = Maze.find_numbers(info_data)
    results = dict()
    for start in numbers:
        if start not in results:
            results[start] = dict()
        for end in numbers:
            if start != end and end not in results.keys():
                print(f"Searching for {start} to {end}")
                m = Maze(info_data, start=numbers[start], goal=numbers[end])
                r = astar(m, Maze.goal, Maze.neighbours, Maze.goal)
                if r is not None:
                    level = 0
                    while r.parent:
                        level += 1
                        r = r.parent
                    results[start][end] = level
                    # results[start][end] = r.level - 1
                else:
                    raise RuntimeError(
                        f"BFS failed to find a path from {start} to {end}"
                    )

    print("completed first section....")

    lowest_result = 1_000_000
    options = permutations(numbers.keys())
    for option in options:
        if option[0] == 0:
            total = 0
            for a, b in zip(option, option[1:]):
                try:
                    total += results[a][b]
                except Exception:
                    # Likely just reversed .. so try again
                    total += results[b][a]
            if back_to_start:
                add_on = option[-1]
                try:
                    total += results[add_on][0]
                except Exception:
                    total += results[0][add_on]

            lowest_result = total if total < lowest_result else lowest_result
    return lowest_result


if __name__ == "__main__":
    test_data = [
        "###########",
        "#0.1.....2#",
        "#.#######.#",
        "#4.......3#",
        "###########",
    ]
    puzzle_data = get_lines(r"./data/day_24.txt")

    travelling_elves(test_data)
    part_01 = travelling_elves(puzzle_data)
    assert part_01 == 498

    part_02 = travelling_elves(puzzle_data, back_to_start=True)
    assert part_02 == 804
