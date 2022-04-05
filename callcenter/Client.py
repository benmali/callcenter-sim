import numpy as np
import math
from helpers import Probabilities, TimeHelper


class Client:
    """
    A class to represent a client
    """

    def __init__(self, arrival_time, sector=None, age=None, contact_method=None, contact_reason=None):
        self.arrival_time = arrival_time
        self.sector = 'Blue-Collar' if np.random.uniform(0, 1) < 0.2 else 'High-Tech'
        self.age = np.random.normal(38, 7)  # avg age is 38, lower bound is 18, upper bound is 60
        self.wait_time = 0
        self.service_time = 0
        self.total_time = 0
        call_probability = np.random.uniform(0, 1)
        if self.age > 35 and self.sector == 'Blue-Collar':  # Older employees tend to call
            if call_probability < 0.8:
                self.contact_method = 'call'
            else:
                self.contact_method = 'chat'
        else:
            if call_probability < 0.4:
                self.contact_method = 'call'
            else:  # 60% are chats
                self.contact_method = 'chat'

        self.contact_reason = 'Where is my food'

    def __repr__(self):
        return f"Client's Arrival: {self.arrival_time}, Method: {self.contact_method}, Reason: {self.contact_reason}"
