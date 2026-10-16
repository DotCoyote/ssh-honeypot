import argparse
from collections import Counter
from honeypot import EVENT_TYPE_COMMAND_INPUT, EVENT_TYPE_LOGIN
from honeypot.export import export_to_csv, generate_csv_data
from honeypot.logs import get_event_by_type, get_top_from_events, read_events
from honeypot.sanitize import cleanup_text

class HoneypotArgs(argparse.Namespace):
    log_path: str
    top: int
    csv: str | None

def define_args() -> argparse.ArgumentParser:
    args_parser = argparse.ArgumentParser(description="Analyze Cowrie honeypot logs")
    args_parser.add_argument('log_path', nargs='?', default="cowrie/logs/cowrie.json", help="Falls back to cowrie/logs/cowrie.json if not provided")
    args_parser.add_argument('-t', '--top', type=int, default=10, help="How many most common items should be shown. Default: 10")
    args_parser.add_argument('--csv', type=str, nargs="?", const="cowrie/export/logs.csv", default=None, help="Should the summary of the logs get exported to a csv file")
    return args_parser

def print_sanitized_logs(entries: list, description: str | None = None) -> None:
    if description:
        print(f"\n{description}")
    for value, count in entries:
        print(f"{cleanup_text(value)} ({count})")

if __name__ == "__main__":
    argument_parser = define_args()
    provided_args = argument_parser.parse_args(namespace=HoneypotArgs())

    all_events, error_count, empty_lines_count = read_events(provided_args.log_path)
    all_logins = get_event_by_type(all_events, EVENT_TYPE_LOGIN)
    all_input_commands = get_event_by_type(all_events, EVENT_TYPE_COMMAND_INPUT)

    username_count = get_top_from_events(all_logins, "username", provided_args.top)
    password_count = get_top_from_events(all_logins, "password", provided_args.top)
    attempt_by_ip_count = get_top_from_events(all_logins, "src_ip", provided_args.top)
    command_input_count = get_top_from_events(all_input_commands, "input", provided_args.top)

    print_sanitized_logs(username_count, "Top Usernames")
    print_sanitized_logs(password_count, "Top Passwords")
    print_sanitized_logs(attempt_by_ip_count, "Top Attempts by IP")
    print_sanitized_logs(command_input_count, "Top Commands")

    if provided_args.csv:
        csv_data = generate_csv_data(username_count, "username")
        csv_data.extend(generate_csv_data(password_count, "password"))
        csv_data.extend(generate_csv_data(attempt_by_ip_count, "src_ip"))
        csv_data.extend(generate_csv_data(command_input_count, "command"))
    
        export_to_csv(csv_data, provided_args.csv)