import os
import random
from ipaddress import IPv4Address
import secrets
import sys
from lesson3 import LOGIN_FAILED_CODE, LOGIN_SUCCESS_CODE, count_values
from lesson7 import cleanup_text, read_events
from lesson5 import group_events_by_session
import datetime as dt
from lesson4 import write_events_to_file
from collections import Counter
import argparse

usernames = ['admin', 'root', 'peter', 'jessica', 'kirk', 'james', 'lars', 'robert']
passwords = ['test1234', 'password123', 'THIS_IS_SAFE', 'sadf0nds9h234n!', 'super-duper-pass', 'pass_me']
SUCCESS_RATE = 0.1

def random_ipv4():
    'Generates a random IP address'
    return str(IPv4Address(random.randint(0, 2**32 - 1)))

def make_session_id():
    'Creates a cryptographically-secure, URL-safe string'
    return secrets.token_urlsafe(16) 

def generate_sessions(amount: int = 20):
    'Generates $amount random sessions'
    sessions = []

    for _ in range(amount):
        sessions.append(dict(id = make_session_id(), src_ip = random_ipv4()))

    return sessions

def sort_by_timestamp(elements: list):
    return sorted(elements, key=lambda d: d['timestamp'])   

def get_values_from_entries(entries: list, value: str):
    return {entry[value] for entry in entries}

def generate_test_data(log_path: str, entries: int = 200) -> None:
    'Generates a synthetic Cowrie log with $entries and writes it to $log_path'
    session_count = entries // 10
    sessions = generate_sessions(session_count)
    data = []
    today = dt.datetime.now(dt.timezone.utc).date()
    midnight = dt.datetime.combine(today, dt.datetime.min.time(), dt.timezone.utc)

    if not log_path.startswith('/'):
        log_path = os.path.join(os.path.dirname(__file__), log_path)

    for session in sessions:
        attempt_count = random.randint(2, 15)
        now = midnight + dt.timedelta(seconds=random.randint(0,86400), milliseconds=random.randint(1,100000))
        for i in range(attempt_count):
            now += dt.timedelta(seconds=random.randint(1, 20))
            succeeds = i == (attempt_count - 1) and random.random() < SUCCESS_RATE
            eventid = LOGIN_SUCCESS_CODE if succeeds else LOGIN_FAILED_CODE
            data.append(dict(
                eventid = eventid,
                username = random.choice(usernames),
                password = random.choice(passwords),
                session = session['id'],
                src_ip = session['src_ip'],
                timestamp = now.isoformat().replace('+00:00', 'Z')
            ))

    sorted_data = sort_by_timestamp(data)
    write_events_to_file(sorted_data, log_path)

def get_all_ips(entries: list):
    return get_values_from_entries(entries, 'src_ip')

def get_successful_ips(entries: list):
    return {entry['src_ip'] for entry in entries if entry['eventid'] == LOGIN_SUCCESS_CODE}

def get_all_as_list(entries: list, key: str):
    return [entry[key] for entry in entries]

def build_username_password_pairs(entries: list):
    return [(entry["username"], entry["password"]) for entry in entries]

def parse_timestamp(timestamp: str):
    return dt.datetime.fromisoformat(timestamp)

def collect_entry_times(entries: list):
    return [parse_timestamp(entry["timestamp"]) for entry in entries]

def session_duration(entries: list):
    session_timestamps = collect_entry_times(entries)
    return max(session_timestamps) - min(session_timestamps)

def format_duration(duration: dt.timedelta):
    "Transforms a duration timedelta to a time-string"
    times = []
    total_seconds = int(duration.total_seconds())
    hours, leftover_minutes_in_seconds = divmod(total_seconds, 3600)
    minutes, leftover_seconds = divmod(leftover_minutes_in_seconds, 60)

    if hours > 0: times.append(f"{hours}h")
    if minutes > 0 or hours > 0: times.append(f"{minutes}m")
    times.append(f"{leftover_seconds}s")

    return " ".join(times)

def calculate_average_session_duration(session_durations: dict[str, dt.timedelta]) -> dt.timedelta:
    "Calculates the average of a dict with timedeltas"
    session_sum = sum(session_durations.values(), dt.timedelta())
    return session_sum // len(session_durations)

def count_hours_from_entries(entry_times: list[dt.datetime]) -> Counter[int]:
    "Returns a Counter of hours in UTC, counted by how many times they appear"
    return Counter(time.hour for time in entry_times)

def generate_full_day_counter(counted_hours: Counter[int]) -> dict[int, int]:
    "Returns a dict containing all hours (0-23) with num of occurred events"
    all_hours = {}
    for hour in range(0, 24):
        all_hours[dt.time(hour=hour).strftime("%H:%M")] = counted_hours[hour]
    return all_hours

if __name__ == "__main__":
    # Parse Arguments
    args_parser = argparse.ArgumentParser(description="Test-Data Generator")
    args_parser.add_argument('logPath', default='data/cowrie_test.json', help="Falls back to data/cowrie_test.json if not provided")
    args_parser.add_argument('-t', '--top', type=int, default=5, help="How many most common items should be shown. Default: 5")
    args_parser.add_argument('-g', '--generate', action='store_true', help="Whether or not to generate a testfile. Overwrites existing files.")
    provided_args = args_parser.parse_args()

    if provided_args.generate is True:
        print(f"Writing Test File {provided_args.logPath}")
        test_data = generate_test_data(provided_args.logPath)

    # With Set
    events, error_count, num_empty_lines = read_events(provided_args.logPath)

    if len(events) < 1:
        print("No events found")
        sys.exit()

    ips = get_all_ips(events)
    sessions = get_values_from_entries(events, 'session')
    print(f"All IPs length: {len(ips)}")
    print(f"Sessions count: {len(sessions)}")

    successful_ips = get_successful_ips(events)
    print(f"Successful IPs length: {len(successful_ips)}")
    print(f"Failed IPs length: {len(ips - successful_ips)}")

    counter_passwords = Counter(get_all_as_list(events, "password"))
    most_common_passwords = counter_passwords.most_common(provided_args.top)
    print(most_common_passwords) # type = list[tuple[str, int]]
    print("Most common passwords:")
    for password, count in most_common_passwords:
        print(f"{cleanup_text(password)} ({count})")

    counter_usernames = Counter(get_all_as_list(events, "username"))
    most_common_usernames = counter_usernames.most_common(provided_args.top)
    print(most_common_usernames) # type = list[tuple[str, int]]
    print("Most common usernames:")
    for username, count in most_common_usernames:
        print(f"{cleanup_text(username)} ({count})")

    print(counter_passwords == count_values(get_all_as_list(events, "password")))

    usernames_with_passwords = Counter(build_username_password_pairs(events))
    most_common_pairs = usernames_with_passwords.most_common(provided_args.top)
    print(most_common_pairs)
    for (username, password), count in most_common_pairs:
        print(f"{cleanup_text(username)}/{cleanup_text(password)}: {count}x")

    print(parse_timestamp("2026-10-09T00:07:30.570000Z").tzinfo) # UTC

    all_times = collect_entry_times(events)
    duration = max(all_times) - min(all_times)

    print(f"Log covers: {min(all_times).strftime("%d.%m.%Y %H:%M:%S %Z")} -> {max(all_times).strftime("%d.%m.%Y %H:%M:%S %Z")} ({format_duration(duration)})")

    print("\n#### STEP 3 ####")
    grouped_events = group_events_by_session(events)
    session_durations = {session_id: session_duration(session_events) for session_id, session_events in grouped_events.items()}

    shortest_session_id = min(session_durations, key=session_durations.__getitem__)
    longest_session_id = max(session_durations, key=session_durations.__getitem__)
    print(f"Shortest Session: {cleanup_text(shortest_session_id)} ({format_duration(session_durations[shortest_session_id])})")
    print(f"Longest Session: {cleanup_text(longest_session_id)} ({format_duration(session_durations[longest_session_id])})")

    print(f"Average Session: {format_duration(calculate_average_session_duration(session_durations))}")

    print("\n#### Step 4: events per hour ####")
    print("Events per hour (UTC):")
    counted_hours = count_hours_from_entries(all_times)
    formatted_full_day_hours = generate_full_day_counter(counted_hours)
    highest_count_width = len(str(max(formatted_full_day_hours.values())))
    for hour, hour_counts in formatted_full_day_hours.items():
        print(f"{hour:6} {hour_counts:{highest_count_width}} {'#'*hour_counts}")

    assert len(all_times) == counted_hours.total()