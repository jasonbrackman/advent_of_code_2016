import helpers
import re


def get_groups_of_data(line):
    pattern = re.compile(r"(\w+)|\[(\w+)]")
    results = pattern.findall(line)
    in_brackets = list()
    out_brackets = list()

    for result in results:
        if result[0]:
            out_brackets.append(result[0])
        if result[1]:
            in_brackets.append(result[1])

    return in_brackets, out_brackets


def supports_tls(lines):

    counter = 0

    for index, line in enumerate(lines):
        should_continue = True
        in_brackets, out_brackets = get_groups_of_data(line)

        for group in in_brackets:
            # print(f"[{index}] {group[1]}")
            if is_palindrome(group):
                should_continue = False
                break

        if should_continue:
            for group in out_brackets:
                if is_palindrome(group):
                    counter += 1
                    break

    return counter


def is_palindrome(group):
    for i in range(len(group)):
        window = group[i : i + 4]
        if len(window) == 4 and window == window[::-1] and len(set(list(window))) == 2:
            return True
    return False


def contains_aba_bab(outside_brackets, inside_brackets):
    abas = list()
    for group in outside_brackets:
        for i in range(len(group)):
            window = group[i : i + 3]
            if (
                len(window) == 3
                and window == window[::-1]
                and len(set(list(window))) == 2
            ):
                abas.append(f"{window[1]}{window[0]}{window[1]}")

    for group in inside_brackets:
        if any(bab in group for bab in abas):
            return True

    return False


def supports_ssl(lines):
    counter = 0

    for index, line in enumerate(lines):
        in_brackets, out_brackets = get_groups_of_data(line)
        if contains_aba_bab(in_brackets, out_brackets):
            counter += 1

    return counter


def main():
    lines = helpers.get_lines(r"./data/day_07.txt")
    part_01 = supports_tls(lines)
    assert part_01 == 110

    part_02 = supports_ssl(lines)
    assert part_02 == 242


if __name__ == "__main__":
    main()
