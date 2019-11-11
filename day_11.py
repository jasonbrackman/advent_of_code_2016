from typing import List, Dict, Tuple
from itertools import combinations
from helpers import bfs, get_node_path_results


class ElevatorState:
    # 1. Start on the first floor
    # 2. Must have a generator or microchip (or both) to run the elevator
    # 3. a microchip cannot be on a floor with a mismatching generator without its sister generator

    def __init__(
        self, cf: int, f1: List[str], f2: List[str], f3: List[str], f4: List[str]
    ):

        self.cf: int = cf
        self.floor: dict = {1: f1, 2: f2, 3: f3, 4: f4}

    def __str__(self) -> str:
        return (
            f"F4 {'E' if self.cf == 4 else '.'}  {self.floor[4]}\n"
            f"F3 {'E' if self.cf == 3 else '.'}  {self.floor[3]}\n"
            f"F2 {'E' if self.cf == 2 else '.'}  {self.floor[2]}\n"
            f"F1 {'E' if self.cf == 1 else '.'}  {self.floor[1]}\n"
        )

    def __hash__(self):
        return hash(str(self))

    def goal(self) -> bool:
        return self.floor[1] == self.floor[2] == self.floor[3] == []

    def is_legal(self) -> bool:
        if not 1 <= self.cf <= 4:
            return False

        for floor in [self.floor[1], self.floor[2], self.floor[3], self.floor[4]]:
            pairs, orphans = self.get_pairs_and_orphans(floor)

            # A microchip and a generator that is not a pair is not allowed on same floor
            if len(set(o[-1] for o in orphans)) == 2:
                return False

            if pairs and any(o.endswith("m") for o in orphans):
                return False

        return True

    def successors(self):
        sucs: List[ElevatorState] = []

        # Get current, lower, and upper floor numbers in short-hand
        cf = self.cf
        lf = cf - 1
        uf = cf + 1

        # get info for options about moving between floors
        pairs, orphans = self.get_pairs_and_orphans(self.floor[cf])

        for (a, b) in combinations(self.floor[cf], 2):
            temp = self.get_window((a, b), lf)
            es = ElevatorState(lf, temp[1], temp[2], temp[3], temp[4])
            if es.is_legal():
                sucs.append(es)

            temp = self.get_window((a, b), uf)
            es = ElevatorState(uf, temp[1], temp[2], temp[3], temp[4])
            if es.is_legal():
                sucs.append(es)

        for orphan in orphans:
            temp = self.get_window((orphan,), lf)
            es = ElevatorState(lf, temp[1], temp[2], temp[3], temp[4])
            if es.is_legal():
                sucs.append(es)

            temp = self.get_window((orphan,), uf)
            es = ElevatorState(uf, temp[1], temp[2], temp[3], temp[4])
            if es.is_legal():
                sucs.append(es)

        return sucs

    def get_window(self, items: Tuple, next_floor) -> Dict[int, List[str]]:
        temp = dict()
        for index in range(1, 5):
            if index == self.cf:
                i = [x for x in self.floor[self.cf] if x not in items]
                temp[index] = sorted(i)
            elif index == next_floor:
                j = list(self.floor[next_floor])
                for item in items:
                    j.append(item)
                temp[index] = sorted(j)
            else:
                temp[index] = list(self.floor[index])

        return temp

    def get_pairs_and_orphans(self, param: List) -> [List, List]:
        pairs = []
        orphans = []
        names = {n[:-1] for n in param}
        for name in names:
            if name + "g" in param:
                if name + "m" in param:
                    pairs.append((name + "g", name + "m"))
                else:
                    orphans.append(name + "g")
            else:
                orphans.append(name + "m")

        return pairs, orphans


if __name__ == "__main__":

    current_floor = 1
    floor_04 = []
    floor_03 = ["lg"]
    floor_02 = ["hg"]
    floor_01 = ["hm", "lm"]
    e = ElevatorState(current_floor, floor_01, floor_02, floor_03, floor_04)
    r = bfs(e, ElevatorState.goal, ElevatorState.successors)
    response = get_node_path_results(r, silent=True)
    # print(response - 1)
    assert response - 1 == 11, f"expected 11, but received [{response}]."

    current_floor = 4
    floor_04 = ["lg"]
    floor_03 = []
    floor_02 = []
    floor_01 = ["lm"]
    e = ElevatorState(current_floor, floor_01, floor_02, floor_03, floor_04)
    r = bfs(e, ElevatorState.goal, ElevatorState.successors)
    response = get_node_path_results(r, silent=True)
    # print(response - 1)
    assert response - 1 == 6

    current_floor = 1
    floor_04 = []
    floor_03 = []
    floor_02 = ["polm", "prom"]
    floor_01 = ["polg", "prog", "tg", "tm", "rg", "rm", "cg", "cm"]
    e = ElevatorState(current_floor, floor_01, floor_02, floor_03, floor_04)
    r = bfs(e, ElevatorState.goal, ElevatorState.successors)

    response = get_node_path_results(r, silent=True)
    # print(response - 1)
    assert response - 1 == 47

    # Part 2
    current_floor = 1
    floor_04 = []
    floor_03 = []
    floor_02 = ["polm", "prom"]
    floor_01 = [
        "polg",
        "prog",
        "tg",
        "tm",
        "rg",
        "rm",
        "cg",
        "cm",
        "eg",
        "em",
        "dg",
        "dm",
    ]
    e = ElevatorState(current_floor, floor_01, floor_02, floor_03, floor_04)
    r = bfs(e, ElevatorState.goal, ElevatorState.successors)

    response = get_node_path_results(r, silent=True)
    # print(response-1)
    assert response - 1 == 71
