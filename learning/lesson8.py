import copy

from dataclasses import dataclass
from lesson3 import LOGIN_SUCCESS_CODE
from lesson7 import cleanup_text
from lesson5 import login_event, connect_event, WEAK_ALGORITHMS

@dataclass
class Event:
    'A class representing a generic event with an event ID, session, and source IP address.'
    eventid: str
    session: str
    src_ip: str
    
    def describe(self):
        'Return a description of the event, including the event ID, source IP, and session.'
        return f"{cleanup_text(self.eventid)} from {cleanup_text(self.src_ip)} (session {cleanup_text(self.session)})"

@dataclass
class LoginEvent(Event):
    'A class representing a login event, inheriting from the Event class, with additional attributes for username, password, and source port.'
    username: str
    password: str
    src_port: int

    def is_success(self):
        'Check if the login event was successful based on the eventid.'
        return self.eventid == LOGIN_SUCCESS_CODE

    def describe(self):
        state = "successful" if self.is_success() else "failed"
        return f"Login {state.upper()}: {cleanup_text(self.username)}/{cleanup_text(self.password)}, IP: {cleanup_text(self.src_ip)} (session {cleanup_text(self.session)})"

    @classmethod
    def from_dict(cls, event_dict):
        'Create a LoginEvent instance from a dictionary containing event data.'
        return cls(
            eventid=event_dict["eventid"],
            username=event_dict["username"],
            password=event_dict["password"],
            session=event_dict["session"],
            src_ip=event_dict["src_ip"],
            src_port=event_dict["src_port"]
        )

@dataclass
class KexEvent(Event):
    'A class representing a key exchange event, inheriting from the Event class, with additional attributes for key exchange algorithms and key algorithms.'
    kexAlgs: list
    keyAlgs: list

    def is_weak_kex(self):
        'Check if the key exchange event uses any weak key exchange algorithms.'
        return any(alg in WEAK_ALGORITHMS for alg in self.kexAlgs)

    def describe(self):
        'Return a description of the key exchange event, including the event ID, source IP, and session.'
        return f"Key exchange from {cleanup_text(self.src_ip)}: {len(self.kexAlgs)} algorithms, weak: {self.is_weak_kex()} (session {cleanup_text(self.session)})"

    @classmethod
    def from_dict(cls, event_dict):
        'Create a KexEvent instance from a dictionary containing event data.'
        return cls(
            eventid=event_dict["eventid"],
            session=event_dict["session"],
            src_ip=event_dict["src_ip"],
            kexAlgs=event_dict["kexAlgs"],
            keyAlgs=event_dict["keyAlgs"]
        )

if __name__ == "__main__":
    login_event_success = copy.deepcopy(login_event)
    login_event_success["eventid"] = LOGIN_SUCCESS_CODE
    login_event_success["src_port"] = 42716
    login_event1 = LoginEvent.from_dict(login_event_success)

    login_event_failed = copy.deepcopy(login_event)
    login_event_failed["src_port"] = 42716
    login_event2 = LoginEvent.from_dict(login_event_failed)

    kex_event = KexEvent.from_dict(connect_event)

    events = [login_event1, login_event2, kex_event]

    for event in events:
        print(event.describe())