import helpers
from collections import Counter


def least_common_repetition(lines):
    collect = list()
    for index in range(len(lines[0])):
        chars = [line[index] for line in lines]
        common = Counter(chars).most_common()[-1]
        print(common)
        collect.append(common[0])

    return "".join(collect)


def most_common_repetition(lines):
    collect = list()
    for index in range(len(lines[0])):
        chars = [line[index] for line in lines]
        most_common = Counter(chars).most_common(1)[0]
        collect.append(most_common[0])

    return "".join(collect)


def test_data():
    lines = helpers.get_lines(r"./data/day_06_test_data.txt")
    test = least_common_repetition(lines)
    assert test == "advent"


if __name__ == "__main__":
    test_data()

    lines = helpers.get_lines(r"./data/day_06.txt")
    part_01 = most_common_repetition(lines)
    assert part_01 == "tsreykjj"

    part_02 = least_common_repetition(lines)
    assert part_02 == "hnfbujie"
