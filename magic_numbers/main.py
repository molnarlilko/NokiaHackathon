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