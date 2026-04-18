from pathlib import Path
import math
from datetime import datetime

FREE_MINS = 30
LOW_RATE = 300
LOW_RATE_HOURS = 3
HIGH_RATE = 500
DAY_CAP = 10_000
DAY_MINS = 24 * 60


def parse_dt(s: str) -> datetime:
    return datetime.strptime(s.strip(), "%Y-%m-%d %H:%M:%S")

def calculate_fee(total_mins: float, per_min: bool = False) -> int:
    if total_mins <= FREE_MINS:
        return 0
    
    full_days = int(total_mins // DAY_MINS)
    remaining = total_mins - full_days * DAY_MINS

    fee = full_days * DAY_CAP

    billable = remaining - FREE_MINS

    if billable <= 0:
        return fee
    
    hours = math.ceil(billable / 60)

    if hours <= LOW_RATE_HOURS:
        partial = hours * LOW_RATE
    else:
        partial = LOW_RATE_HOURS * LOW_RATE + (hours - LOW_RATE_HOURS) * HIGH_RATE

    fee += min(partial, DAY_CAP)

    return fee


def main():
    data = Path("input.txt").read_text(encoding="utf-8")
    
    results = []
    for line in data.splitlines():
        s = line.strip()
        if not s or s.startswith("=") or "RENDSZAM" in s.upper():
            continue

        parts = [p.strip() for p in s.split("\t") if p.strip()]
        if len(parts) < 3:
            continue

        plate = parts[0]
        try:
            entry = parse_dt(parts[1])
            exit_ = parse_dt(parts[2])
        except ValueError:
            results.append(f"{plate}\tHibás dátum formátum")
            continue

        if exit_ < entry:
            results.append(f"{plate}\tKijárat nem lehet korábbi, mint a bejárat")
            continue

        minutes = (exit_ - entry).total_seconds() / 60
        results.append(f"{plate}\t\t{calculate_fee(minutes)}")
 
    out = "RENDSZAM\tDIJ\n" + "\n".join(results)
    print(out)
    Path("output.txt").write_text(out + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()