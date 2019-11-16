def get_next_elf(from_index, elves):
    while True:
        if elves[from_index] > 0:
            return from_index, elves[from_index]
        from_index = (from_index + 1) % len(elves)


def steal_from_right(puzzle_input):
    elves = {x: 1 for x in range(puzzle_input)}
    count = 0
    while True:
        fk, fv = get_next_elf(count, elves)
        sk, sv = get_next_elf((fk + 1) % len(elves), elves)

        if (fk, fv) == (sk, sv):
            return fk + 1

        else:
            elves[fk] += sv
            elves[sk] = 0
            count = (sk + 1) % len(elves)


if __name__ == "__main__":
    puzzle_input = 3017957
    part_01 = steal_from_right(puzzle_input)
    assert part_01 == 1841611
