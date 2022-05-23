import numpy as np
from helpers import Probabilities
import datetime


class ClientMetric:
    def __init__(self, contact_method, contact_reason, client_type, sector, arrival_time, wait_time, service_time, abandoned=False, abandon_time=None):
        self.contact_method = contact_method
        self.contact_reason = contact_reason
        self.client_type = client_type
        self.sector = sector
        self.arrival_time = arrival_time
        self.wait_time = wait_time
        self.service_time = service_time
        self.abandoned = abandoned
        self.abandoned_time = abandon_time

    def __repr__(self):
        if self.abandoned:
            return f"Method: {self.contact_method}, Reason: {self.contact_reason}, Type: {self.client_type}, Sector: {self.sector}, Arrival: {self.arrival_time}, Wait: {self.wait_time}, Service: {self.service_time / 60}, Abandoned: Yes, Abandon Time:{self.abandoned_time}"
        else:
            return f"Method: {self.contact_method}, Reason: {self.contact_reason}, Type: {self.client_type}, Sector: {self.sector}, Arrival: {self.arrival_time}, Wait: {self.wait_time}, Service: {self.service_time / 60}, Abandoned: No"


class Client:
    """
    A class to represent a client
    """

    def __init__(self, arrival_time, client_type='Client', sector=None, age=None, contact_method=None, contact_reason=None):
        self.arrival_time = arrival_time
        self.sector = 'Blue-Collar' if np.random.uniform(0, 1) < 0.2 else 'High-Tech'
        self.age = np.random.normal(38, 7)  # avg age is 38, lower bound is 18, upper bound is 60
        self.wait_time = 0
        self.service_time = 0
        self.total_time = 0
        self.client_type = client_type
        self.abandoned = False
        self.abandon_time = None
        self.max_wait_time = Probabilities.max_client_patience()
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

        if self.age > 45 and self.sector == 'Blue-Collar' and np.random.uniform(0, 1) < 0.8:
            self.contact_reason = 'Reset Password'
        else:
            self.contact_reason = 'Where is my food'

        if client_type == 'Restaurant':
            self.sector = 'Restaurant'
            self.contact_method = 'call'
            self.contact_reason = 'Out of ingredient'

    def __repr__(self):
        return f"Client's Arrival: {self.arrival_time}, Method: {self.contact_method}, Reason: {self.contact_reason}"

    def update_metrics(self, start_service_time: datetime.datetime, contact_duration):
        self.set_wait_time(start_service_time)
        self.set_service_time(contact_duration)

    def abandon_queue(self):
        self.abandoned = True
        self.abandon_time = self.arrival_time + self.max_wait_time
        self.wait_time = self.max_wait_time

    def get_metrics(self):
        """
        Get metrics from client
        Times in Minutes
        @return:
        """
        if self.abandoned:
            metric = ClientMetric(self.contact_method, self.contact_reason, self.client_type, self.sector, self.arrival_time, self.wait_time.total_seconds() / 60, self.service_time, self.abandoned, self.abandon_time)
        else:
            metric = ClientMetric(self.contact_method, self.contact_reason, self.client_type, self.sector,
                                  self.arrival_time, self.wait_time.total_seconds() / 60, self.service_time,
                                  False)
        return metric

    def set_wait_time(self, start_service_time: datetime.datetime):
        """
        Update client's total waiting time when he starts to get service
        @param start_service_time:
        @return:
        """
        self.wait_time = start_service_time - self.arrival_time

    def set_service_time(self, service_time: float):
        """
        Set service time for client
        @param service_time:
        @return:
        """
        self.service_time = service_time