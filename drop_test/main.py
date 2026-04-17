from pathlib import Path


def min_num_of_drops(NumberOfDrop, Height):
    dp = [0] * (NumberOfDrop + 1)
    trials = 0

    while dp[NumberOfDrop] < Height:
        trials += 1
        for i in range(NumberOfDrop, 0, -1):
            dp[i] = dp[i] + dp[i-1] + 1

    return trials


def main():
    lines = Path("input.txt").read_text(encoding="utf-8").splitlines()

    for line in lines:
        line = line.strip()
        if not line:
            continue

        NumberOfDrops_str, Height_str = line.split(",")
        NumberOfDrops = int(NumberOfDrops_str.strip())
        Height = int(Height_str.strip())

        print(min_num_of_drops(NumberOfDrops, Height))


if __name__ == "__main__":
    main()