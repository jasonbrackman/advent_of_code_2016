import re
from hashlib import md5

needle3 = re.compile(r"(.)\1{2}")
needle5 = re.compile(r"(.)\1{4}")


def stretch(start):
    for x in range(2016):
        start = md5(start.encode()).hexdigest()
    return start


def yield_number(start: int):
    while True:
        yield start
        start += 1


def yield_hash(salt, stretched=False):
    for index in yield_number(0):
        key = f"{salt}{index}".encode()
        md5_hash = md5(key).hexdigest()
        if stretched:
            md5_hash = stretch(md5_hash)

        # need to check length of five first
        result = re.findall(needle5, md5_hash)
        if result:

            yield (index, result[0] * 5, md5_hash)

        # if it fell through it might be a length of three
        result = re.findall(needle3, md5_hash)
        if result:
            # print(md5_hash, result)
            yield (index, result[0] * 3, md5_hash)


def find_keys(salt, stretched):
    hashes = yield_hash(salt, stretched=stretched)
    found = []
    visited = []
    while len(found) < 65:
        i, key, h = next(hashes)
        if len(key) == 5:
            for v in sorted(visited, key=lambda x: x[0]):
                if i - 1000 < v[0] < i and v[1] == key[0] * 3:
                    if v not in found:
                        found.append(v)
        else:
            visited.append((i, key))

    return found


if __name__ == "__main__":
    salt = "yjdafjpo"
    # salt = "abc"

    found = find_keys(salt, stretched=False)
    for i, v in enumerate(sorted(set(found), key=lambda x: x[0]), 1):
        if i == 64:
            print("Part01 =", i, v)

    found = find_keys(salt, stretched=True)
    for i, v in enumerate(sorted(set(found), key=lambda x: x[0]), 1):
        if i == 64:
            print("Part02 =", i, v)
