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





if __name__ == "__main__":
    process_parking_file("parking_input.txt", "parking_output.txt")
