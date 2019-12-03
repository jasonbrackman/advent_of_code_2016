import day_23

puzzle_path = r"./data/day_25.txt"
part_01 = None
for index in range(0, 1_000_000):
    try:
        m = day_23.Machine(puzzle_path, a=index)
    except Exception as e:
        # print(index, e)
        if "[0, 1, 0, 1, 0, 1, 0, 1, 0, 1]" in str(e):
            part_01 = index
            break
print("Part01:", part_01)
