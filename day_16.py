import copy


def modified_dragon_curve(data):
    """
    Call the data you have at this point "a".
    Make a copy of "a"; call this copy "b".
    Reverse the order of the characters in "b".
    In "b", replace all instances of 0 with 1 and all 1s with 0.
    The resulting data is "a", then a single 0, then "b".
    """
    a = data
    b = "".join([("1" if x == "0" else "0") for x in a[::-1]])
    return f"{a}0{b}"


def checksum(data):
    # Take a window of two characters and see if they repeat
    # 00 or 11 -> 1
    # 01 or 10 -> 0
    value = ""
    for index in range(0, len(data), 2):
        window = data[index : index + 2]
        window = set(window)
        result = "1" if len(window) == 1 else "0"
        value += result

    if len(value) % 2 == 0:
        value = checksum(value)

    return value


def test_modified_dragon_curve():
    assert modified_dragon_curve("1") == "100"
    assert modified_dragon_curve("0") == "001"
    assert modified_dragon_curve("11111") == "11111000000"
    assert modified_dragon_curve("111100001010") == "1111000010100101011110000"


def test_checksum():
    assert checksum("110010110100") == "100"


def test_aoc_item():
    result = "10000"
    while len(result) < 20:
        result = modified_dragon_curve(result)
    result = result[:20]
    assert result == "10000011110010000111"
    assert checksum(result) == "01100"


def part_01(data, length):
    while len(data) < length:
        data = modified_dragon_curve(data)
    data = data[:length]
    return checksum(data)


if __name__ == "__main__":
    test_modified_dragon_curve()
    test_checksum()
    test_aoc_item()

    puzzle_input = "10001001100000001"
    length = 272
    print(f"Part01: {part_01(puzzle_input, length)}")

    length = 35651584
    print(f"Part02: {part_01(puzzle_input, length)}")
