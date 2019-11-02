import helpers
import re
from collections import deque


class Grid:
    pattern = re.compile(
        r"^rect (?P<recx>\d+)\w(?P<recy>\d+)|"
        r"^rotate (?P<rot>row|column) \w=(?P<roty>\d+) by (?P<rotcount>\d+)"
    )

    def __init__(self, x, y, instructions):
        self.cells = [["."] * x for i in range(y)]
        for instruction in instructions:
            # print("Processing:", instruction)
            self.process_instruction(instruction)

    def process_instruction(self, instruction):
        groups = self.pattern.search(instruction)

        if groups["recx"] is not None:
            self.rect(groups["recx"], groups["recy"])

        if groups["rot"] is not None:
            direction = groups["rot"]
            y = int(groups["roty"])
            count = int(groups["rotcount"])
            self.rotate(direction, y, count)

    def rect(self, x, y):
        cols = int(x)
        rows = int(y)
        for row in range(rows):
            for col in range(cols):
                self.cells[row][col] = "#"
        # print(self.cells)

    def rotate(self, direction, rhs, count):
        rhs = int(rhs)
        if direction == "row":
            t = deque(self.cells[rhs])
            t.rotate(count)
            self.cells[rhs] = list(t)

        else:
            chars = deque([self.cells[i][rhs] for i, _ in enumerate(self.cells)])
            chars.rotate(count)
            for i, _ in enumerate(self.cells):
                self.cells[i][rhs] = chars[i]

    def __str__(self):
        results = ""
        for row in self.cells:
            results += " ".join(row)
            results += "\n"
        return results[:-1]


if __name__ == "__main__":

    data = helpers.get_lines(r"./data/day_08.txt")

    g = Grid(50, 6, data)
    total = 0
    for row in g.cells:
        total += row.count("#")
    assert total == 115

    expected = [
        "# # # #   # # # #   # # # #   #       # #     #   # # # #   # # #     # # # #     # # #       # #  \n",
        "#         #         #         #       # #   #     #         #     #   #             #           #  \n",
        "# # #     # # #     # # #       #   #   # #       # # #     #     #   # # #         #           #  \n",
        "#         #         #             #     #   #     #         # # #     #             #           #  \n",
        "#         #         #             #     #   #     #         #   #     #             #     #     #  \n",
        "# # # #   #         # # # #       #     #     #   #         #     #   #           # # #     # #    ",
    ]

    assert str(g).replace(".", " ") == "".join(expected)  # EFEYKFRFIJ ?
