from datetime import datetime
from math import ceil
from pathlib import Path


def calculate_parking_fee(total_minutes: int) -> int:

    if total_minutes < 0:
        return -1

    if total_minutes <= 30:
        return 0

    minutes_per_day = 24 * 60
    if total_minutes >= minutes_per_day:
        blocks = ceil(total_minutes / minutes_per_day)
        return blocks * 10000

    chargeable = total_minutes - 30
    hours = ceil(chargeable / 60)

    cheap_hours = min(hours, 3)
    expensive_hours = max(0, hours - 3)

    fee = cheap_hours * 300 + expensive_hours * 500
    return fee


def parse_line(line: str):
    line = line.strip()
    if not line:
        return None

    parts = line.split()
    if len(parts) < 5:
        return None

    plate = parts[0]
    arrival_str = parts[1] + " " + parts[2]
    departure_str = parts[3] + " " + parts[4]

    try:
        arrival = datetime.strptime(arrival_str, "%Y-%m-%d %H:%M:%S")
        departure = datetime.strptime(departure_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return {
            "plate": plate,
            "fee": "HIBAS DATUM"
        }

    delta = departure - arrival
    total_minutes = int(delta.total_seconds() // 60)

    if total_minutes < 0:
        return {
            "plate": plate,
            "fee": "HIBAS IDOREND"
        }

    fee = calculate_parking_fee(total_minutes)

    return {
        "plate": plate,
        "fee": fee
    }


def process_parking_file(input_path: str, output_path: str):
    in_file = Path(input_path)
    if not in_file.exists():
        print(f"Nem található a bemeneti fájl: {input_path}")
        return

    lines = in_file.read_text(encoding="utf-8", errors="ignore").splitlines()
    results = []

    for line in lines:
        if "RENDSZAM" in line and "ERKEZES" in line and "TAVOZAS" in line:
            continue
        if set(line.strip()) == {"="}:
            continue

        parsed = parse_line(line)
        if parsed:
            results.append(parsed)

    out_lines = []

    for r in results:
        plate = r["plate"]
        fee = r["fee"]
        out_lines.append(f"{plate} → {fee} forint")

    Path(output_path).write_text("\n".join(out_lines), encoding="utf-8")
    print(f"Eredmény kiírva ide: {output_path}")

