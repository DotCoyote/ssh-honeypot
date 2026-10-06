import json
import os

from lesson3 import filter_events, count_values, loginattempts, LOGIN_SUCCESS_CODE, LOGIN_FAILED_CODE

passwords_file_name = "passwords.txt"
data_folder_path = os.path.join(os.path.dirname(__file__), "data")
passwords_file_path = os.path.join(data_folder_path, passwords_file_name)
cowrie_log_file_name = "cowrie_sample.json"
cowrie_log_file_path = os.path.join(data_folder_path, cowrie_log_file_name)

passwords = [
    "password123",
    "qwerty",
    "letmein",
    "admin",
    " adm ",
    "bomb",
    "womb",
    "welcome",
    "monkey",
    "abc123",
    "password1"
]

event_dict = dict(eventid=LOGIN_FAILED_CODE, something=True, elsething=None, username='admin', password='123456', src_ip='1.2.3.4', src_port=42716)

def is_weak(password, min_length=6):
    'Check if a password is weak (less than specified number of characters)'
    return len(password) < min_length

def write_lines_to_file(lines, file_path):
    'Write each line to the file'
    with open(file_path, "w", encoding="utf-8") as passwords_file:
        for line in lines:
            passwords_file.write(line + "\n")

def append_lines_to_file(lines, file_path):
    'Write each line to the file'
    with open(file_path, "a", encoding="utf-8") as passwords_file:
        for line in lines:
            passwords_file.write(line + "\n")

def read_lines_from_file(file_path):
    'Read lines from the file and return them as a list'
    with open(file_path, "r", encoding="utf-8") as passwords_file:
        return [line.rstrip("\n") for line in passwords_file]

def write_events_to_file(events: list, file_path: str):
    'Write events to the file in JSON format'
    event_list = [json.dumps(event) for event in events]
    write_lines_to_file(event_list, file_path)

def read_events_from_file(file_path: str):
    'Read events from the file and return them as a list of dictionaries'
    with open(file_path, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f]

def print_successful_logins(events: list):
    'Print successful login events'
    for event in filter_events(events, LOGIN_SUCCESS_CODE):
        print(f"Successful login: {event['username']} from {event['src_ip']}")

def assemble_passwords_from_logs(events: list):
    'Assemble a list of passwords from login events'
    return [event['password'] for event in events]

if __name__ == "__main__":
    # Ensure the data folder exists
    os.makedirs(data_folder_path, exist_ok=True)

    # Write each password to the file, one per line
    write_lines_to_file(passwords, passwords_file_path)

    passwords = read_lines_from_file(passwords_file_path)
    # Read the passwords from the file and print them
    for password in passwords:
        if is_weak(password):
            print(f"Password '{password}' is weak.")

    print(event_dict)
    jsonstr = json.dumps(event_dict, indent=4)
    print(jsonstr)

    decoded_dict = json.loads(jsonstr)
    print(decoded_dict, type(decoded_dict))
    print(type(json.dumps(event_dict, indent=4)))

    write_events_to_file(loginattempts, cowrie_log_file_path)

    read_loginattempts = read_events_from_file(cowrie_log_file_path)
    print_successful_logins(read_loginattempts)

    used_passwords = assemble_passwords_from_logs(read_loginattempts)
    print(count_values(used_passwords))