from pathlib import Path

def main():
    lines = Path("input.txt").read_text(encoding="utf-8").splitlines()

    for line in lines:
        line = line.strip()

        if "^" in line:
            base, exp = line.split("^")
            n = int(base) ** int(exp)
        else:
            n = int(line)

        print(next_magic_num(n))

if __name__ == "__main__":
    main()

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