from hashlib import md5


def get_next(counter):
    while True:
        yield counter
        counter += 1


def solve(start):
    for i in get_next(0):
        result = md5(f"{start}{i}".encode()).hexdigest()
        if result.startswith("00000"):
            yield result


def part_02(start):
    results = [" "] * 8
    for result in solve(start):
        pos, char = result[5], result[6]

        try:
            if results[int(pos)] == " ":
                results[int(pos)] = char
        except (ValueError, IndexError):
            pass

        if " " not in results:
            return "".join(results)


def part_01(start):
    results = list()
    for result in solve(start):
        results.append(result)
        if len(results) == 8:
            return "".join([h[5] for h in results])


if __name__ == "__main__":
    p1 = part_01("ugkcyxxp")
    assert p1 == "d4cd2ee1"

    p2 = part_02("ugkcyxxp")
    assert p2 == "f2c730e5"
