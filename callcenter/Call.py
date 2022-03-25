
class Call:
    def __init__(self, call_time, call_reason, call_date, from_rest: bool = False, total_time: float = 0):
        """
        Class to create a Call object
        Call can be created by (Agent, Restaurant, Client) in any direction
        :param call_time: Time client called
        :param call_reason: Reason for the call
        :param call_date: Date of the call
        :param total_time: Total time (seconds) the call took
        """
        self.call_reason = call_reason  # Where is my food, Password reset, dish complaint, app issues, order rules (blue collar)
        self.call_time = call_time  # Time
        self.call_date = call_date
        self.source = None
        self.destination = None
        self.from_rest = from_rest  # This will be used to create a priority queue

    def __lt__(self, other):
        """
        Sort call order - call that arrived first will be answered first
        """
        # R R
        # R N
        # N R
        # N N
        if self.from_rest and not other.from_rest:
            return True
        elif not self.from_rest and other.from_rest:
            return False
        else:
            return self.call_time < other.call_time

