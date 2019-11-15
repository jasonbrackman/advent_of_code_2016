class Disc:
    def __init__(self, pos: int, turns: int):
        self.start_pos = pos
        self.pos = pos
        self.turns = turns

    def tick(self, index):
        self.pos = (self.start_pos + index) % self.turns

    def __repr__(self):
        return f"Disc({self.start_pos}, {self.turns}) @ pos[{self.pos}]"


def spin_tumbler(discs):
    time = 1

    while True:
        possible = True
        for index, disc in enumerate(discs, 1):
            disc.tick(time + index)
            if disc.pos != 0:
                possible = False

        if possible:
            # print(f"Time [{time}]: {discs}")
            return time
        time += 1


if __name__ == "__main__":

    # tests = [
    #     Disc(4, 5),
    #     Disc(1, 2),
    # ]
    # spin_tumbler(tests)

    part1 = [
        Disc(10, 13),
        Disc(15, 17),
        Disc(17, 19),
        Disc(1, 7),
        Disc(0, 5),
        Disc(1, 3),
    ]
    part_01 = spin_tumbler(part1)
    assert part_01 == 203660

    part2 = [
        Disc(10, 13),
        Disc(15, 17),
        Disc(17, 19),
        Disc(1, 7),
        Disc(0, 5),
        Disc(1, 3),
        Disc(0, 11),  # new
    ]
    part_02 = spin_tumbler(part2)
    assert part_02 == 2408135
