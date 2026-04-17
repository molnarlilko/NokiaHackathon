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


if __name__ == "__main__":
    process_parking_file("parking_input.txt", "parking_output.txt")
