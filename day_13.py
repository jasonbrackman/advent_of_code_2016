from helpers import bfs, get_node_path_results


def is_a_space(x, y, puzzle_input=1358):
    result = bin(x * x + 3 * x + 2 * x * y + y + y * y + puzzle_input).count("1")
    return result % 2 == 0


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

        if wx >= 0 and is_a_space(wx, cy):
            sucs.append(MazeState((wx, cy), self.goal_position))
        if ny >= 0 and is_a_space(cx, ny):
            sucs.append(MazeState((cx, ny), self.goal_position))

        if is_a_space(ex, cy):
            sucs.append(MazeState((ex, cy), self.goal_position))
        if is_a_space(cx, sy):
            sucs.append(MazeState((cx, sy), self.goal_position))

        return sucs


if __name__ == "__main__":

    e = MazeState((1, 1), (31, 39))
    r = bfs(e, MazeState.goal, MazeState.successors, by_level=50)
    part_01 = r.level - 1  # don't count the initial node space
    print(f"Part01: {part_01}")
