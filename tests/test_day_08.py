import unittest
import day_08


class TestDay08(unittest.TestCase):
    def test_grid_rect(self) -> None:
        instructions = ["rect 3x2"]
        grid = day_08.Grid(7, 3, instructions)
        total = 0
        for row in grid.cells:
            total += row.count("#")
        self.assertEqual(total, 6)

    def test_grid_rect_rotate(self):
        instructions = [
            "rect 3x2",
            "rotate column x=1 by 1",
            "rotate row y=0 by 4",
            "rotate column x=1 by 1",
        ]
        grid = day_08.Grid(7, 3, instructions)
        total = 0
        for row in grid.cells:
            total += row.count("#")

        expected = ". # . . # . #\n# . # . . . .\n. # . . . . ."
        self.assertEqual(expected, str(grid))


if __name__ == "__main__":
    unittest.main()
