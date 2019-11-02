import unittest
import day_07


class TestDay07(unittest.TestCase):
    data = [
        "abba[mnop]qrst supports",
        "abcd[bddb]xyyx",
        "aaaa[qwer]tyui",
        "ioxxoj[asdfgh]zxcvbn",
        "sdfs[fsdf]wer[ewer]fff",
    ]

    def test_parse_line(self):
        for line in self.data:
            groups = day_07.find_square_brackets(line)
            for group in groups:
                print(group)

        """
         TLS (abba outside square brackets).
         does not support TLS (bddb is within square brackets, even though xyyx is outside square brackets).
         does not support TLS (aaaa is invalid; the interior characters must be different).
         supports TLS (oxxo is outside square brackets, even though it's within a larger string).
        """


if __name__ == "__main__":
    unittest.main()
