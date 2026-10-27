import math
import sys

HEATING_STEP = 0.5  # degrees gained per slice while heating
COOLING_STEP = 0.5  # degrees lost per slice while cooling
DRIFT_STEP = 0.25   # degrees moved toward outside per slice while idle
MINUTES_PER_SLICE = 30
MINUTES_PER_DAY = 24 * 60   # 1440


def clock(minute_of_day):
    """750 -> '12:30'"""
    hours, minutes = divmod(minute_of_day, 60)
    return f"{hours:02d}:{minutes:02d}"


def decide(indoor, tmin, tmax):
    if indoor < tmin:
        return "heating"
    if indoor > tmax:
        return "cooling"
    return "nothing"


def update(indoor, outside, action):
    if action == "heating":
        indoor += HEATING_STEP
    elif action == "cooling":
        indoor -= COOLING_STEP
    else:
        # Idle: the house slowly converges to the outside temperature.
        if indoor < outside:
            indoor += DRIFT_STEP
        elif indoor > outside:
            indoor -= DRIFT_STEP
    return indoor


def main():
    if len(sys.argv) != 3:
        raise SystemExit(
            "Usage: python3 expert_system.py <minimum temp> <maximum temp>"
        )

    try:
        tmin = float(sys.argv[1])
        tmax = float(sys.argv[2])
    except ValueError:
        raise SystemExit("Error: thresholds must be numbers.")

    if not math.isfinite(tmin) or not math.isfinite(tmax):
        raise SystemExit("Error: thresholds must be finite numbers.")

    if tmin >= tmax:
        raise SystemExit(
            "Error: the minimum threshold must be lower than the maximum."
        )

    indoor = None
    minute_of_day = 0

    try:
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            try:
                outside = float(line)
            except ValueError:
                continue  # not a temperature, ignore the line
            if not math.isfinite(outside):
                continue  # ignore NaN and infinite readings

            if indoor is None:
                indoor = outside  # first reading: indoor starts at outside

            action = decide(indoor, tmin, tmax)
            indoor = update(indoor, outside, action)

            print(f"time: {clock(minute_of_day)} - temp. outside: {outside:.2f} - {action} - temp. inside: {indoor:.2f}")
            minute_of_day = (minute_of_day + MINUTES_PER_SLICE) % MINUTES_PER_DAY

    except KeyboardInterrupt:
        print("\nSimulation stopped.", file=sys.stderr)



if __name__ == "__main__":
    main()
