from collections import Counter
import json

from honeypot import EVENT_TYPE_LOGIN
from honeypot.sanitize import cleanup_text

def read_events(path: str):
    "Read events from the given log file and return a list of events, skips broken lines, returns the number of errors encountered. Prints errors to the console including line numbers."

    events = list()
    errors = list()
    empty_lines = 0
    with open(path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, start=1):
            if not line.strip():
                empty_lines += 1
                continue
            try:
                event = json.loads(line.strip())
            except json.JSONDecodeError as e:
                errors.append((line.strip(), e))
                print(f"Error decoding JSON on line {line_num}: {cleanup_text(line.strip())} - {e}")
            else: 
                events.append(event)
    return events, len(errors), empty_lines

def get_event_by_type(events: list, event_type: str) -> list:
    "Filters a list of cowrie events and returns only events with given type"
    return [event for event in events if event["eventid"].startswith(event_type)]

def get_values_as_list(entries: list, key: str):
    "Gets the value of a list of entry and checks if that value actually exists"
    return [entry[key] for entry in entries if key in entry]

def get_top_from_events(events: list, key: str, top: int = 10) -> list[tuple[str, int]]:
    "Returns top N elements from an event list"
    return Counter(get_values_as_list(events, key)).most_common(top)