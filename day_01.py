import helpers
import re

rotation = {
    'R': 1,
    'L': -1,
}

names = {
    0: "North",
    1: "East",
    2: "South",
    3: "West",
}

arrows = {
    0: (-1, 0),
    1: (0, 1),
    2: (1, 0),
    3: (0, -1),
}


def get_directions():
    lines = helpers.get_lines(r"./data/day_01.txt")
    directions = lines[0].split(", ")
    return directions


def parse_directions(directions):
    pattern = re.compile(r'(\w)(\d+)')
    parsed = list()
    for d in directions:
        results = pattern.search(d)
        x, y = results.groups()
        parsed.append((x, y))

    return parsed


def add_positions(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2

    return x1+x2, y1+y2


def get_shortest_path(directions, first_visit_stop=False):
    pos = (0, 0)
    compass = 0

    visited = {pos}
    for (x, y) in directions:
        compass = (compass + rotation[x]) % 4
        for i in range(int(y)):
            pos = add_positions(pos, arrows[compass])
            if first_visit_stop and pos in visited:
                return abs(pos[0]) + abs(pos[1])
            visited.add(pos)
        # print(f"{d} | {names[compass]} => {pos}")
    return abs(pos[0]) + abs(pos[1])



def main():
    directions = get_directions()
    directions = parse_directions(directions)
    part01 = get_shortest_path(directions)
    print("Part01 => Total Distance:", part01)

    part02 = get_shortest_path(directions, first_visit_stop=True)
    print("Part02 => Total Distance:", part02)


if __name__ == "__main__":
    main()
