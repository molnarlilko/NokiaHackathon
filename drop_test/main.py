from pathlib import Path


def main():
    lines = Path("input.txt").read_text(encoding="utf-8").splitlines()

    for line in lines:
        line = line.strip()
        if not line:
            continue

        NumberOfDrops_str, Height_str = line.split(",")
        NumberOfDrops = int(NumberOfDrops_str.strip())
        Height = int(Height_str.strip())

if __name__ == "__main__":
    main()