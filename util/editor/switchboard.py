from collections import deque

class Event:
    def __init__(self, type: str, data: dict = None):
        self.type = type
        self.data = data

    def __repr__(self):
        return f"Event({self.type}, {self.data})"

class Switchboard:
    def __init__(self):
        self._events = deque()
    
    def add_event(self, event: Event):
        self._events.append(event)
    
    def get_event(self) -> Event:
        if self._events:
            return self._events.popleft()
        return None

    def has_events(self) -> bool:
        return bool(self._events)
