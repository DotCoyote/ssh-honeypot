import json
import os

log_path = os.path.join(os.path.dirname(__file__), "data", "test_log_lesson7.json")

PREVIEW_MAX_LENGTH = 100
REQUIRED_FIELDS = ["eventid", "username", "password", "src_ip", "src_port"]

def validate_event(event: dict, required_fields: list):
    'Check if the event has all required fields. Raises ValueError if any are missing, otherwise returns True.'
    missing_fields = [field for field in required_fields if field not in event]
    if missing_fields:
        raise ValueError(f"Missing fields: {', '.join(missing_fields)}")
    return True

def cleanup_text(text: str, max_length: int = PREVIEW_MAX_LENGTH):
    'Clean up the text for display, truncating it if it exceeds max_length and appending an ellipsis and the number of truncated characters.'
    if len(text) > max_length:
        return repr(text[:max_length]) + "... (+" + str(len(text) - max_length) + " chars)"
    return repr(text)

def read_events(path: str):
    'Read events from the given log file and return a list of events, skips broken lines, returns the number of errors encountered. Prints errors to the console including line numbers.'

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
                print(f"Error decoding JSON on line {line_num}: {cleanup_text(line.strip(), PREVIEW_MAX_LENGTH)} - {e}")
            else: 
                events.append(event)
    return events, len(errors), empty_lines

def validate_events(events: list, required_fields: list):
    'Validate events and return a list of valid events, skips invalid events, returns the number of errors encountered. Prints errors to the console including line numbers.'
    valid_events = list()
    errors = list()
    for line_num, event in enumerate(events, start=1):
        try:
            validate_event(event, required_fields)
        except ValueError as e:
            errors.append((event, e))
            print(f"Error validating event #{line_num}: {cleanup_text(json.dumps(event), PREVIEW_MAX_LENGTH)} - {e}")
        else:
            valid_events.append(event)
    return valid_events, len(errors)

if __name__ == "__main__":
    events, num_errors, num_empty_lines = read_events(log_path)
    valid_events, num_validation_errors = validate_events(events, REQUIRED_FIELDS)
    print(f"Read {len(events)} events, with {num_errors} errors and {num_empty_lines} empty lines.")
    print(f"Number of validation errors: {num_validation_errors}")

    for event in valid_events:
        print(f"Valid event: {cleanup_text(event['username'])}/{cleanup_text(event['password'])} from {cleanup_text(event['src_ip'])}:{event['src_port']}")