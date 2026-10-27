import math
import sys
import time
from enum import Enum


class Season(Enum):
    SPRING = (6, 24)
    SUMMER = (18, 35)
    AUTUMN = (5, 20)
    WINTER = (-10, 8)


def get_season():
    if len(sys.argv) < 2:
        raise SystemExit(
            "Usage: python main.py <season|1-4>\n"
            "Seasons: 1 = spring, 2 = summer, 3 = autumn, 4 = winter"
        )

    user_input = sys.argv[1].strip()

    # Allow choosing a season by its number.
    season_numbers = {
        "1": Season.SPRING,
        "2": Season.SUMMER,
        "3": Season.AUTUMN,
        "4": Season.WINTER,
    }

    if user_input in season_numbers:
        return season_numbers[user_input]

    # Allow choosing a season by its name.
    try:
        return Season[user_input.upper()]
    except KeyError:
        raise SystemExit(
            "Invalid season. Choose spring, summer, autumn, winter "
            "or a number from 1 to 4."
        )


def get_temperature(season, hour):
    minimum, maximum = season.value

    average = (minimum + maximum) / 2
    amplitude = (maximum - minimum) / 2

    # Minimum around 00:00, maximum around 12:00
    temperature = average + amplitude * math.cos(
        2 * math.pi * (hour - 15) / 24
    )

    return temperature


def simulate_day(season):
    hour = 0.0

    try:
        while True:
            temperature = get_temperature(season, hour)

            # flush=True: a pipe is block-buffered, so without this the
            # expert system would wait ages for each reading.
            print(f"{temperature:.2f}", flush=True)
            # Advance simulated time by 30 minutes.
            hour = (hour + 0.5) % 24

            # Wait one real second (one slice = 30 simulated minutes).
            time.sleep(1)

    except KeyboardInterrupt:
        # stderr, so it never pollutes the pipe of temperatures.
        print("\nSimulation stopped.", file=sys.stderr)


if __name__ == "__main__":
    season = get_season()
    simulate_day(season)