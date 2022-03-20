class Call:
    def __init__(self, call_time, call_reason, call_date):
        """
        Class to create a Call object
        :param call_time: Total time (seconds) the call took
        :param call_reason: Reason for the call
        :param call_date: Date of the call
        """
        self.call_reason = call_reason  # Where is my food, Password reset, dish complaint, app issues, order rules (blue collar)
        self.call_time = call_time
        self.call_date = call_date

