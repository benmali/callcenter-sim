class Event:
    def __init__(self, time, event_type, client=None, agent=None):
        """
        :param time: system time
        :param event_type: event types
        """
        self.time = time
        self.event_type = event_type
        self.client = client
        self.agent = agent

    def __lt__(self, other):
        return self.time < other.time

    def __repr__(self):
        return f"{self.time} : {self.event_type}"
