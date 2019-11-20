import helpers

max = 4294967295

last_i = -1
last_o = -1

# Parse the data
lines = helpers.get_lines(r"./data/day_20.txt")

stuff = list()
for line in lines:
    i, o = line.split("-")
    i, o = int(i), int(o)
    stuff.append((i, o))

# Collect Gaps
allowed = list()
for line in sorted(stuff):
    i, o = line

    if last_o >= i or i == last_o + 1:
        last_i = i
        if o > last_o:
            last_o = o
    else:
        for i in range(last_o + 1, i):
            allowed.append(i)
        last_i = i
        last_o = o

print("Part_01:", allowed[0])

# max might not have been hit so check it.
part_02 = len(allowed) + max - last_o
print("Part_02:", part_02)
