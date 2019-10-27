import unittest
import day_01


class TestDay01(unittest.TestCase):
    def test_main_12(self):
        directions = ['R5', 'L5', 'R5', 'R3']
        result = day_01.get_shortest_path(directions)
        self.assertEqual(12, result)

    def test_main_2(self):
        directions = ['R2', 'R2', 'R2']
        result = day_01.get_shortest_path(directions)
        self.assertEqual(2, result)

    def test_main_5(self):
        directions = ['R2', 'L3']
        result = day_01.get_shortest_path(directions)
        self.assertEqual(5, result)


if __name__ == "__main__":
    unittest.main()
