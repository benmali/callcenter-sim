class Event:
    def __init__(self, time, event_type):
        """
        :param time: system time
        :param event_type: event types
        """
        self.time = time
        self.event_type = event_type

    def __lt__(self, other):
        return self.time < other.time

    def __repr__(self):
        return f"{self.time} : {self.event_type}"
