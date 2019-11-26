from helpers import bfs, get_lines, get_node_path_results, astar
import re
from itertools import permutations
from typing import List, Optional, Tuple
from copy import deepcopy

needle = re.compile(r".*x(\d+)-y(\d+)")


class Node:
    def __init__(self, name: str, used: int, avail: int):
        self.name = name
        self.used = used
        self.avail = avail

    def __hash__(self):
        return hash(self.name) + hash(self.used) + hash(self.avail)

    def __str__(self):
        return f"Node('{self.name}', '{self.used}', '{self.avail}')"

    def is_valid_pair(self, other) -> bool:
        if self.used == 0:
            return False

        if hash(self) == hash(other):
            return False

        if self.used > other.avail:
            return False

        return True


class PuzzleState:

    target = (0, 0)

    def __init__(self, initial_state_path, goal):
        # goal is the Node that should be moved to 0, 0
        self.goal = goal

        # Setup initial state of the board
        self.maze_state: List[List[Node]] = []
        self.init_puzzle_state(initial_state_path)

    def __hash__(self):
        empty = self.identify_pos()
        goal = self.identify_pos(self.goal)
        return hash((empty, goal))

    def __str__(self):
        space_pos = self.identify_pos()
        buffer = "-" * 45
        for y, items in enumerate(self.maze_state):
            buffer += "\n"
            for x, item in enumerate(items):
                if (x, y) == space_pos:
                    buffer += "O"
                elif y == x == 0:
                    buffer += "T"
                elif hash(item) == hash(self.goal):
                    buffer += "G"
                else:
                    x_pos, y_pos = space_pos
                    space_node = self.maze_state[y_pos][x_pos]
                    buffer += "." if item.is_valid_pair(space_node) else "#"
        buffer += "\n"
        # buffer += f"Hash: {hash(self)}\n"
        buffer += f"Heuristic: {self.heuristic()}"

        return buffer

    def identify_pos(self, node=None) -> Tuple[int, int]:
        for y, items in enumerate(self.maze_state):
            for x, item in enumerate(items):
                if node is None and item.used == 0:
                    return x, y
                else:
                    if node and hash(node) == hash(item):
                        return x, y

    def heuristic(self):

        # Manhattan Distance
        x1, y1 = self.identify_pos()
        x2, y2 = self.identify_pos(self.goal)
        x_dist: int = abs(x1 - (x2 - 1))
        y_dist: int = abs(y1 - y2)

        return x_dist + y_dist

    def goal(self):
        return self.identify_pos(self.goal) == (0, 0)

    def successors(self):
        # Try and move the target to the goal
        # If it can't be moved -- let's move the closest empty container to the space that the
        #  target is interested in --

        sucs = []
        # 1. try moving that goal to the left
        x, y = self.identify_pos(self.goal)
        if self.goal.is_valid_pair(self.maze_state[y][x - 1]):
            board = deepcopy(self)
            PuzzleState.swap_positions(board, (x, y), (x - 1, y))
            sucs.append(board)

        else:
            # find space and its neighbors and see if we can move it...
            x, y = self.identify_pos()
            space_node = self.maze_state[y][x]
            up = (y - 1, x)
            down = (y + 1, x)
            left = (y, x - 1)
            right = (y, x + 1)

            for y_dir, x_dir in [up, down, left, right]:
                # ensure that the number is in bounds of the board
                if 0 <= y_dir < len(self.maze_state) and 0 <= x_dir < len(
                    self.maze_state[0]
                ):
                    node_temp = self.maze_state[y_dir][x_dir]
                    if node_temp.is_valid_pair(space_node) and hash(node_temp) != hash(
                        self.goal
                    ):
                        # need the cost of the move of the space to this location
                        board = deepcopy(self)
                        PuzzleState.swap_positions(board, (x, y), (x_dir, y_dir))
                        sucs.append(board)

        return sucs

    def init_puzzle_state(self, init_save_path):
        lines = get_lines(init_save_path)
        i_lines = iter(lines)

        # skip command line
        next(i_lines)

        # skip header
        next(i_lines).split()

        for line in i_lines:
            node_name, size, used, avail, percentage = line.split()
            # x = int(needle.search(node_name).group(1))
            y = int(needle.search(node_name).group(2))

            if len(self.maze_state) == y:
                self.maze_state.append([])

            new_node = Node(node_name, int(used[:-1]), int(avail[:-1]))

            self.maze_state[y].append(new_node)

    def get_valid_pairs(self):
        nodes = list()
        for items in self.maze_state:
            for item in items:
                nodes.append(item)

        count = 0
        for (a, b) in permutations(nodes, 2):
            if a.is_valid_pair(b):
                count += 1

        return count

    def investigate(self):
        last_node = self.maze_state[0][-1]
        print(last_node)

        for i in range(29, -1, -1):
            # print(i)
            t = self.maze_state[35][27]
            x = self.maze_state[0][29]
            y = self.maze_state[0][i - 1]
            print(x.is_valid_pair(y), y.used + y.avail)
            print("Can Move Into Space:", y.is_valid_pair(t))
        for i in self.maze_state:
            for col in i:
                if col.avail >= 72:
                    print(True, col)

    @staticmethod
    def swap_positions(board, pos1, pos2):
        x1, y1 = pos1
        x2, y2 = pos2
        board.maze_state[y1][x1], board.maze_state[y2][x2] = (
            board.maze_state[y2][x2],
            board.maze_state[y1][x1],
        )


if __name__ == "__main__":

    goal_node = Node("/dev/grid/node-x35-y0", 65, 27)
    m = PuzzleState(r"./data/day_22.txt", goal_node)

    # goal_node = Node("/dev/grid/node-x2-y0", 6, 4)
    # m = PuzzleState(r"./data/day_22_test.txt", goal_node)
    # print(m)
    # for x in m.successors():
    #     print(x)
    r = astar(m, PuzzleState.goal, PuzzleState.successors, PuzzleState.heuristic)
    print(r)
    if r:
        count = 0
        while r.parent:
            count += 1
            r = r.parent
        print(f"Completed Part 2 in {count} steps.")
    # get_node_path_results(r)

    # part one
    part_01 = m.get_valid_pairs()
    print("Part01:", part_01)
