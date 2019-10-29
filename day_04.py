import re
import helpers
from collections import Counter
from string import ascii_lowercase


def part_02(lines):
    for (items, sector, hash_) in yield_items_sector_hash(lines):
        rotate = int(sector) % 26
        new_word = ""
        for x in " ".join(items):
            if x == " ":
                new_word += x
            else:
                result = (ascii_lowercase.find(x) + rotate) % 26
                new_word += ascii_lowercase[result]
        if "northpole object storage" in new_word:
            return sector

    # print(test, rotate)


def yield_items_sector_hash(lines):
    pattern = re.compile(r"^(\d+)\[(\w+)]")
    for line in lines:
        items = line.split("-")
        sector, hash_ = pattern.search(items[-1]).groups()
        yield items[:-1], sector, hash_


def part_01(lines):
    total = 0

    idata = yield_items_sector_hash(lines)
    for (items, sector, hash_) in idata:
        count = Counter("".join(items))
        result = sorted(count.items(), key=lambda item: (-item[1], item[0]))
        if "".join([c for c, n in result[:5]]) == hash_:
            total += int(sector)

    return total


if __name__ == "__main__":
    lines = helpers.get_lines("./data/day_04.txt")
    assert part_01(lines) == 185371
    assert part_02(lines) == "984"
