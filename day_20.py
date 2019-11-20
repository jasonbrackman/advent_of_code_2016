import helpers

last_i = -1
max = 4294967295
lines = helpers.get_lines(r"./data/day_20.txt")

last_o = -1

stuff = list()
for line in lines:
    i, o = line.split("-")
    i, o = int(i), int(o)
    stuff.append((i, o))

for line in sorted(stuff):
    print(line)

allowed = list()
for line in sorted(stuff):
    # print(line)
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
print("Part_02:", len(allowed))
