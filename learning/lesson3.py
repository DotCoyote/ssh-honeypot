passwords = ['pass', 'word', 'pass', 'password', '1234556', 'password123']
usernames = ['admin', 'user1', 'user2', 'admin', 'user1']

LOGIN_SUCCESS_CODE = 'cowrie.login.success'
LOGIN_FAILED_CODE = 'cowrie.login.failed'

loginattempts = []
loginattempts.append(dict(eventid=LOGIN_FAILED_CODE, username='admin', password='123456', src_ip='1.2.3.4', src_port=42716))
loginattempts.append(dict(eventid=LOGIN_FAILED_CODE, username='admin1', password='78456', src_ip='1.2.3.4', src_port=42716))
loginattempts.append(dict(eventid=LOGIN_SUCCESS_CODE, username='admin2', password='237564', src_ip='1.2.3.4', src_port=42716))
loginattempts.append(dict(eventid=LOGIN_FAILED_CODE, username='admin3', password='pass', src_ip='1.2.3.4', src_port=42716))

def is_weak(password, min_length=6):
    'Check if a password is weak (less than specified number of characters)'
    return len(password) < min_length

def count_values(items):
    'Count the occurrences of each value in a list'
    counts = dict()
    for item in items:
        counts[item] = counts.get(item, 0) + 1
    return counts

def filter_events(events, eventid):
    'Filter events by event ID'
    return [event for event in events if event['eventid'] == eventid]

def format_event(event):
    'Format an event for display'
    return f"Event: {event['eventid']}, User: {event['username']}, Password: {event['password']}, IP: {event['src_ip']}"

def testfunc():
    foo = 'bar'

# print(foo) # NameError: name 'foo' is not defined

def no_return_fn():
    2 + 2

if __name__ == "__main__":
    print(no_return_fn()) # None

    for password in passwords:
        if is_weak(password):
            print(f"Password '{password}' is weak.")

    print(count_values(usernames))

    for event in filter_events(loginattempts, LOGIN_SUCCESS_CODE):
        print(format_event(event))