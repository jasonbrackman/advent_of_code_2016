from hashlib import md5
from helpers import bfs, get_node_path_results


class MazeState:
    maze = [
        "#########",
        "#S| | | #",
        "#-#-#-#-#",
        "# | | | #",
        "#-#-#-#-#",
        "# | | | #",
        "#-#-#-#-#",
        "# | | |  ",
        "####### V",
    ]

    def __init__(self, pos, data, reached_goal=False):
        self.pos = pos
        self.data = data
        self.reached_goal = reached_goal

    def __str__(self):
        return f"{self.pos} -> {self.data}"

    def __hash__(self):
        return hash(self.pos) + hash(self.data) + hash(self.reached_goal)

    def md5_passcode(self):
        return md5(self.data.encode()).hexdigest()

    @staticmethod
    def get_options(code):
        up, down, left, right = code[:4]
        up = True if up in ["b", "c", "d", "e", "f"] else False
        down = True if down in ["b", "c", "d", "e", "f"] else False
        left = True if left in ["b", "c", "d", "e", "f"] else False
        right = True if right in ["b", "c", "d", "e", "f"] else False

        return up, down, left, right

    @staticmethod
    def calculate_new_pos(old_pos, new_pos):
        return old_pos[0] + new_pos[0], old_pos[1] + new_pos[1]

    def goal(self):
        if self.reached_goal is True:
            return False

        result = self.maze[self.pos[0] + 1][self.pos[1] + 1] == "V"
        self.reached_goal = result
        return result

    def successors(self):
        code = self.md5_passcode()
        up_dir = (-1, 0)
        down_dir = (1, 0)
        left_dir = (0, -1)
        right_dir = (0, 1)

        up, down, left, right = self.get_options(code)

        sucs = []

        if up is True:
            self._apply_rules(sucs, up_dir, "U")
        if down is True:
            self._apply_rules(sucs, down_dir, "D")
        if right is True:
            self._apply_rules(sucs, right_dir, "R")
        if left is True:
            self._apply_rules(sucs, left_dir, "L")

        return sucs

    def _apply_rules(self, sucs, direction, postfix):
        row, col = self.calculate_new_pos(self.pos, direction)
        if row < len(self.maze) and col < len(self.maze[0]):
            next_pos = self.maze[row][col]
            if next_pos in ["-", "|"]:
                pos = self.calculate_new_pos((row, col), direction)
                sucs.append(MazeState(pos, self.data + postfix, self.reached_goal))

            if next_pos in ["S", " ", "V"]:
                sucs.append(
                    MazeState((row, col), self.data + postfix, self.reached_goal)
                )


if __name__ == "__main__":
    # test_input = "ihgpwlah"
    # test_input = "ulqzkmiv"
    # m = MazeState((1, 1), test_input)
    # r = bfs(m, MazeState.goal, MazeState.successors, debug=False)
    # print(f"Test01: {r.state}")

    puzzle_input = "ioramepc"
    m = MazeState((1, 1), puzzle_input)
    r = bfs(m, MazeState.goal, MazeState.successors, debug=False)
    print("Part01: ", r.state.data.split(puzzle_input)[1])

    puzzle_input = "ioramepc"
    m = MazeState((1, 1), puzzle_input)
    try:
        r = bfs(
            m,
            MazeState.goal,
            MazeState.successors,
            min_path_length=1_000_000,
            debug=False,
        )
        print(r.state)
    except AttributeError as e:
        print("Part02: ", e)
