import helpers


class Network:
    output = dict()
    bots = dict()

    def __init__(self):
        self.populate_instructions()
        self.process_instructions()

    def process_instructions(self):
        visited = list()
        keep_going = True
        while keep_going:
            keep_going = False
            for key, values in self.bots.items():
                if key not in visited:
                    if len(values["values"]) == 2:
                        visited.append(key)
                        min_ = min(values["values"])
                        max_ = max(values["values"])

                        type_, id_ = values["min"]
                        if type_ == "bot":
                            self.bots[id_]["values"].append(min_)
                        else:
                            self.output[id_] = min_

                        type_, id_ = values["max"]
                        if type_ == "bot":
                            self.bots[id_]["values"].append(max_)
                        else:
                            self.output[id_] = max_
                        keep_going = True

    def populate_instructions(self):
        lines = helpers.get_lines(r"./data/day_10.txt")
        for line in lines:
            src_type, src_value, cmd, *args = line.split()
            src_value = int(src_value)

            if cmd == "goes":
                bot_id = int(args[2])
                if bot_id not in self.bots:
                    self.bots[bot_id] = {"values": [src_value], "min": (), "max": ()}
                else:
                    self.bots[bot_id]["values"].append(src_value)

            if cmd == "gives":
                low_name, low_value = args[2], int(args[3])
                max_name, max_value = args[7], int(args[8])
                if src_value not in self.bots:
                    self.bots[src_value] = {
                        "values": [],
                        "min": (low_name, low_value),
                        "max": (max_name, max_value),
                    }
                else:
                    self.bots[src_value]["min"] = (low_name, low_value)
                    self.bots[src_value]["max"] = (max_name, max_value)

    def get_part_01(self):
        for k, v in self.bots.items():
            if v["values"] == [17, 61] or v["values"] == [61, 17]:
                return k
        return None

    def get_part_02(self):
        a = self.output[0]
        b = self.output[1]
        c = self.output[2]
        return a * b * c


if __name__ == "__main__":
    n = Network()
    part_01 = n.get_part_01()
    assert part_01 == 113

    part_02 = n.get_part_02()
    assert part_02 == 12803
