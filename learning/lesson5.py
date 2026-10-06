import json
import copy

from lesson3 import LOGIN_SUCCESS_CODE, LOGIN_FAILED_CODE

KEY_EXCHANGE_EVENT = "cowrie.client.kex"
SESSION_IDS = ["9032jdm2030932me", "9032jdm2030932mgfd"]

connect_event = dict(
    eventid=KEY_EXCHANGE_EVENT, 
    session=SESSION_IDS[0], 
    src_ip="1.2.3.4", 
    kexAlgs=["curve25519-sha256", "diffie-hellman-group14-sha1", "diffie-hellman-group1-sha1"], 
    keyAlgs=["ssh-ed25519", "ssh-rsa"]
)

login_event = dict(
    eventid=LOGIN_FAILED_CODE,
    session=SESSION_IDS[0],
    username="admin",
    password="123456",
    src_ip="1.2.3.4",
    geoip=dict(
        country_name="Germany", 
        city_name="Berlin", 
        location=dict(
            lat=52.5200, 
            lon=13.4050
        )
    )
)
login_event_without_geoip = copy.deepcopy(login_event)
login_event_without_geoip["session"] = SESSION_IDS[1]
login_event_without_geoip.pop("geoip", None)

connect_event2 = copy.deepcopy(connect_event)
connect_event2["session"] = SESSION_IDS[1]

connect_event3 = copy.deepcopy(connect_event)
connect_event3["session"] = SESSION_IDS[1]
connect_event3["kexAlgs"] = ["curve25519-sha256", "diffie-hellman-group14-sha1"]

connect_event4 = copy.deepcopy(connect_event)
connect_event4["session"] = SESSION_IDS[1]
connect_event4["kexAlgs"] = ["curve25519-sha256"]



event_list = [
    connect_event,
    login_event,
    login_event_without_geoip,
    connect_event2,
    connect_event3,
    connect_event4
]

WEAK_ALGORITHMS = ["diffie-hellman-group1-sha1"]

def get_country(event: dict):
    'Get the country name from the event, return "unknown" if not available'
    return event.get("geoip", {}).get("country_name", "unknown")

def uses_weak_kex_algorithms(event: dict):
    'Check if the event uses weak key exchange algorithms'
    return any(alg in WEAK_ALGORITHMS for alg in event.get("kexAlgs", []))

def group_events_by_session(events: list):
    'Group events by session ID'
    grouped = {}
    for event in events:
        session_id = event["session"]
        if session_id not in grouped:
            grouped[session_id] = []
        grouped[session_id].append(event)
    return grouped

def print_grouped_events(grouped_events: dict):
    'Print grouped events by session ID'
    for session_id, events in grouped_events.items():
        print(f"Session logs: {session_id}, {len(events)} events")

if __name__ == "__main__":
    print(f"Connect event: {json.dumps(connect_event, indent=2)}")
    print(f"Login event: {json.dumps(login_event, indent=2)}")
    print(f"Login event without geoip: {json.dumps(login_event_without_geoip, indent=2)}")

    print(f"Login Country: {get_country(login_event)}")
    print(f"Login Country (with geoip missing): {get_country(login_event_without_geoip)}")
    print(f"Login Latitude: {login_event['geoip']['location']['lat']}, Longitude: {login_event['geoip']['location']['lon']}")
    print(f"Connect first kexAlg: {connect_event['kexAlgs'][0]}")
    print(f"Connect last kexAlg: {connect_event['kexAlgs'][-1]}")
    print(f"Connect key Algorithm counts: {len(connect_event['keyAlgs'])}")

    print(f"Connect uses weak kex algorithms: {uses_weak_kex_algorithms(connect_event)}")
    for alg in connect_event['kexAlgs']:
        print(f"Connect kexAlg: {alg}")

    print_grouped_events(group_events_by_session(event_list))