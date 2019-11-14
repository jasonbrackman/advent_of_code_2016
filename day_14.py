from hashlib import md5
import re

salt = "yjdafjpo"
# salt = "abc"

needle3 = re.compile(r"(.)\1{2}")
needle5 = re.compile(r"(.)\1{4}")


def yield_number(start: int):
    while True:
        yield start
        start += 1


def yield_hash():
    for index in yield_number(0):
        key = f"{salt}{index}".encode()
        md5_hash = md5(key).hexdigest()

        # need to check length of five first
        result = re.findall(needle5, md5_hash)
        if result:

            yield (index, result[0] * 5, md5_hash)

        # if it fell through it might be a length of three
        result = re.findall(needle3, md5_hash)
        if result:
            # print(md5_hash, result)
            yield (index, result[0] * 3, md5_hash)


if __name__ == "__main__":
    hashes = yield_hash()
    found = []
    visited = []
    while len(found) < 65:
        i, key, h = next(hashes)
        if len(key) == 5:
            for v in sorted(visited, key=lambda x: x[0]):
                if i - 1000 < v[0] < i and v[1] == key[0] * 3:
                    # print(v[0], i-1000, i)
                    if v not in found:
                        found.append(v)
        else:
            visited.append((i, key))


if __name__ == "__main__":
    for i, v in enumerate(sorted(set(found), key=lambda x: x[0]), 1):
        if i == 64:
            print(i, v)
