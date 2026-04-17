from pathlib import Path

def next_magic_num(n):
    s = str(n)
    length = len(s)
    half = length // 2

    if length % 2 == 0:
        left_part = s[:half]
        first_try = left_part + left_part[::-1]
    else:
        left_part = s[:half+1]
        first_try = left_part + left_part[:-1][::-1]

    if int(first_try) > n:
        return int(first_try)

    added_to_left = str(int(left_part) + 1)

    if length % 2 == 0:
        second_try = added_to_left + added_to_left[::-1]
    else:
        second_try = added_to_left + added_to_left[:-1][::-1]

    if len(added_to_left) > len(left_part):
        return int("1" + ("0" * (length - 1)) + "1")

    return int(second_try)


def main():
    for line in Path("input.txt").read_text(encoding="utf-8").splitlines():
        line = line.strip()

        n = int(line.split("^")[0]) ** int(line.split("^")[1]) if "^" in line else int(line)

        print(next_magic_num(n))


if __name__ == "__main__":
    main()
