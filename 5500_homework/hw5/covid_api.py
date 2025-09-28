# hw5
import os
import json
from collections import defaultdict
from datetime import datetime
import cloudscraper

# ---------- File locations ----------
# HERE = the folder this .py file is in
HERE = os.path.dirname(__file__)
# STATES_FILE = full path to the text file with the state codes
STATES_FILE = os.path.join(HERE, "states_territories-1.txt")
# DATA_DIR = folder where JSON files will be saved
DATA_DIR = os.path.join(HERE, "data")
# BASE_URL = base link to the API, where {code} will be replaced with "ut", "ny", etc.
BASE_URL = "https://api.covidtracking.com/v1/states/{code}/daily.json"


# ---------- Utilities ----------
def yyyymmdd_to_date(yyyymmdd_int):
    """Turn numbers like 20201231 into a date object (2020-12-31)."""
    s = str(yyyymmdd_int)
    return datetime.strptime(s, "%Y%m%d").date()


def month_key(date_obj):
    """Take a date like 2020-12-31 and return (2020, 12)."""
    return date_obj.year, date_obj.month


def month_str(key_tuple):
    """Turn (year, month) into 'Month YYYY' (example: (2020, 12) -> 'December 2020')."""
    y, m = key_tuple
    return f"{datetime(y, m, 1):%B %Y}"


# ---------- Step 1: Load states/territories ----------
HERE = os.path.dirname(__file__)
STATES_FILE = os.path.join(HERE, "states_territories-1.txt")

def load_states():
    # Print out debug info so you know what folder/file it’s trying to read
    print(f"[debug] __file__ folder: {HERE}")
    print(f"[debug] expecting states file at: {STATES_FILE}")

    # If the file does not exist, just return Utah so the program can still run
    if not os.path.exists(STATES_FILE):
        print("[warn] states_territories-1.txt not found at that path.")
        print("[warn] Falling back to Utah only so you can proceed.")
        return [{"code": "ut", "name": "Utah"}]

    # Try to print the first few lines of the file so you can check format
    try:
        with open(STATES_FILE, "r", encoding="utf-8") as f:
            peek = [next(f, "").rstrip("\n") for _ in range(5)]
        print("[debug] first lines in file:")
        for i, line in enumerate(peek, 1):
            print(f"  {i:>2}: {line}")
    except Exception as e:
        print(f"[warn] could not read file preview: {e}")

    # Now actually read all the states into a list
    states = []
    seen = set()  # keep track so we don’t add duplicates
    with open(STATES_FILE, "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            # Different files might use comma, pipe, semicolon, or just spaces
            if "," in line:
                code, name = line.split(",", 1)
            elif "|" in line:
                code, name = line.split("|", 1)
            elif ";" in line:
                code, name = line.split(";", 1)
            else:
                parts = line.split()
                if len(parts) < 2:
                    continue
                code, name = parts[0], " ".join(parts[1:])

            # Clean up code and name
            code = code.strip().lower()
            name = name.strip()

            # Only accept if code is 2 letters and not already seen
            if len(code) != 2 or not code.isalpha():
                continue
            if code in seen:
                continue

            states.append({"code": code, "name": name})
            seen.add(code)

    # If still no states, fall back to Utah
    if not states:
        print("[warn] Parsed 0 entries. Falling back to Utah only.")
        return [{"code": "ut", "name": "Utah"}]

    # Warn if not the expected 55
    if len(states) != 55:
        print(f"[warn] expected 55 entries, parsed {len(states)}. Proceeding anyway.")

    return states


# ---------- Step 2: Fetch & Save JSON ----------
def fetch_and_save_all(states):
    """
    For each state/territory, go to the API, grab the data, and save it into data/<code>.json.
    """
    os.makedirs(DATA_DIR, exist_ok=True)  # make data folder if it doesn’t exist
    scraper = cloudscraper.create_scraper()  # scraper handles Cloudflare

    for st in states:
        code = st["code"]
        url = BASE_URL.format(code=code)  # plug state code into the URL

        try:
            resp = scraper.get(url, timeout=30)  # ask for the data
            resp.raise_for_status()
            data = resp.json()  # turn response into Python list/dict

            outpath = os.path.join(DATA_DIR, f"{code}.json")
            # save the JSON into a file
            with open(outpath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)

            print(f"Saved {code}.json with {len(data)} records")
        except Exception as e:
            # If something goes wrong (like bad internet), print error
            print(f"Failed to fetch {code}: {e}")
            # If there’s no local file either, just skip it
            outpath = os.path.join(DATA_DIR, f"{code}.json")
            if not os.path.exists(outpath):
                continue


def load_state_json(code):
    """Open a saved JSON file for a state and load it into Python."""
    path = os.path.join(DATA_DIR, f"{code}.json")
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# ---------- Step 3: Compute Stats ----------
def compute_stats(records):
    """
    Do the math for averages, highest day, lowest month, etc.
    Takes a list of records (from the JSON) and returns a dictionary of stats.
    """
    if not records:
        return {
            "avg_daily": 0.0,
            "max_day": None,
            "latest_zero_day": None,
            "best_month": "None",
            "worst_month": "None",
        }

    # Sort records by date from oldest to newest
    rows = sorted(records, key=lambda r: r.get("date", 0))

    # Make a list of (date, new_cases)
    daily = []
    for r in rows:
        d_raw = r.get("date")
        if d_raw is None:
            continue
        try:
            d = yyyymmdd_to_date(d_raw)
        except Exception:
            continue

        # get new cases; if missing or negative, set to 0
        pi = r.get("positiveIncrease")
        val = 0 if pi is None else int(pi)
        if val < 0:
            val = 0
        daily.append((d, val))

    if not daily:
        return {
            "avg_daily": 0.0,
            "max_day": None,
            "latest_zero_day": None,
            "best_month": "None",
            "worst_month": "None",
        }

    # Average = sum of all new cases / number of days
    values = [v for _, v in daily]
    avg_daily = sum(values) / len(values)

    # Find the max new cases and the first date it happened
    max_val = max(values)
    max_day = next(d for d, v in daily if v == max_val)

    # Look backwards for the most recent day with 0 new cases
    latest_zero_day = None
    for d, v in reversed(daily):
        if v == 0:
            latest_zero_day = d
            break

    # Group totals by month
    monthly = defaultdict(int)
    for d, v in daily:
        monthly[month_key(d)] += v

    # Find biggest and smallest month totals
    max_total = max(monthly.values()) if monthly else 0
    min_total = min(monthly.values()) if monthly else 0

    # Pick the earliest month if there’s a tie
    best_month_key = min([k for k, s in monthly.items() if s == max_total]) if monthly else None
    worst_month_key = min([k for k, s in monthly.items() if s == min_total]) if monthly else None

    best_month = month_str(best_month_key) if best_month_key else "None"
    worst_month = month_str(worst_month_key) if worst_month_key else "None"

    return {
        "avg_daily": avg_daily,
        "max_day": max_day,
        "latest_zero_day": latest_zero_day,
        "best_month": best_month,
        "worst_month": worst_month,
    }


# ---------- Step 4: Print Report ----------
def print_report(state_name, state_code, stats):
    def dstr(d):
        return d.strftime("%Y-%m-%d") if d else "None"

    # Print results in the format the assignment asks for
    print("Covid confirmed cases statistics")
    print(f"State name: {state_name} ({state_code.upper()})")
    print("Average number of new daily confirmed cases for the entire state dataset: "
          f"{stats['avg_daily']:.2f}")
    print(f"Date with the highest new number of covid cases: {dstr(stats['max_day'])}")
    print(f"Most recent date with no new covid cases: {dstr(stats['latest_zero_day'])}")
    print(f"Month and Year, with the highest new number of covid cases: {stats['best_month']}")
    print(f"Month and Year, with the lowest new number of covid cases: {stats['worst_month']}")
    print()  # blank line between states


# ---------- Main ----------
def main():
    # Step 1: get the list of states
    states = load_states()

    # Step 2: fetch/save JSON for all states (skip if already saved)
    fetch_and_save_all(states)

    # Step 3: for each state, load JSON, calculate stats, print report
    for st in states:
        code = st["code"]
        name = st["name"]
        data = load_state_json(code)
        stats = compute_stats(data)
        print_report(name, code, stats)


if __name__ == "__main__":
    main()
