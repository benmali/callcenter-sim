import numpy as np
from helpers import Probabilities, TimeHelper


class Client:
    """
    A class to represent a client
    """

    def __init__(self, arrival_time, sector, age, contact_method, contact_reason):
        self.sector = sector
        self.age = age
        self.arrival_time = arrival_time
        self.wait_time = 0
        self.service_time = 0
        self.total_time = 0
        self.contact_method = contact_method  # Set to call or chat
        self.contact_reason = contact_reason  # where_is_my_food, forgot_password, login_issues

    def __repr__(self):
        return f"Client's Arrival: {self.arrival_time}, Method: {self.contact_method}, Reason: {self.contact_reason}"
