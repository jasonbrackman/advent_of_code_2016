from helpers import bfs, get_node_path_results


def get_space_type(x, y, puzzle_input=1358):
    result = bin(x * x + 3 * x + 2 * x * y + y + y * y + puzzle_input).count("1")
    return "." if result % 2 == 0 else "#"


# fewest number of steps required for you to reach 31,39
class MazeState:
    puzzle_input = 1358  # 10

    def __init__(self, start, goal):
        self.start = start
        self.goal_position = goal

    def __str__(self):
        return f"Current Position: {self.start}"

    def __hash__(self):
        return hash(self.start)

    def goal(self):
        return self.start == self.goal_position

    def successors(self):
        sucs = []

        cx, cy = self.start
        wx = cx - 1
        ex = cx + 1
        ny = cy - 1
        sy = cy + 1

        if wx >= 0 and get_space_type(wx, cy) == ".":
            sucs.append(MazeState((wx, cy), self.goal_position))
        if ny >= 0 and get_space_type(cx, ny) == ".":
            sucs.append(MazeState((cx, ny), self.goal_position))

        if get_space_type(ex, cy) == ".":
            sucs.append(MazeState((ex, cy), self.goal_position))
        if get_space_type(cx, sy) == ".":
            sucs.append(MazeState((cx, sy), self.goal_position))

        return sucs


if __name__ == "__main__":

    e = MazeState((1, 1), (31, 39))
    r = bfs(e, MazeState.goal, MazeState.successors)
    response = get_node_path_results(r, silent=False)
    print(f"Part01: {response - 1}")
