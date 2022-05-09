import datetime
from collections import defaultdict

import numpy as np

class Metrics:
    def __init__(self, metric_date: datetime.datetime):
        self.metric_date = metric_date
        self.total_calls = 0
        self.total_chats = 0
        self.calls = []  # Store whole tuple of data
        self.chats = []  # Store whole tuple of data
        self.chat_durations = []
        self.call_durations = []
        self.number_of_calls = 0
        self.number_of_chats = 0
        self.call_wait_times = []
        self.chat_wait_times = []  # call_id: (enter time+date, duration waited)
        self.n_rejected_calls = 0  #
        self.agent_starvation = {}  # time agent had no work (waited for work)
        self.queue_lengths = {}  # Time: (len(call_queue), len(chat_queue)
        self.chat_client_abandoned = 0
        self.call_client_abandoned = 0
        self.arrival_histogram = defaultdict(int)
    # Number of end employees ratio to agents
    # What is the number of agents needed to provide SLA when a new company of size X signs?

    def add_call_or_chat(self, client_data):
        contact_method = client_data.contact_method
        if contact_method == "call":
            self.calls.append(client_data)
            # add other stuff here
        else:
            self.chats.append(client_data)

    def add_abandonment(self, client_data):
        contact_method = client_data.contact_method
        if contact_method == "call":
            self.call_client_abandoned += 1
            # add other stuff here
        else:
            self.chat_client_abandoned +=1

    def get_contact_reason_breakdown(self, contact_method):
        """
        Return call reason: number of clients
        @return:
        """
        contact_reason = defaultdict(int)
        if contact_method == 'call':
            contacts = self.calls
        else:
            contacts = self.chats
        for contact in contacts:
            contact_reason[contact.contact_reason] += 1
        return dict(contact_reason)

    def get_rest_calls(self):
        return [call for call in self.calls if call.client_type == 'Restaurant']

    def get_rest_wait_histogram(self):
        """
        Get number of rest waiting specific time
        @return:
        """
        rest_calls_hist = defaultdict(int)
        for call in self.get_rest_calls():

            rest_calls_hist[round(call.wait_time, 2)] += 1
        return rest_calls_hist

    def get_client_calls(self):
        return [call for call in self.calls if call.client_type != 'Restaurant']

    def get_client_call_wait_histogram(self):
        """
        Get number of rest waiting specific time
        @return:
        """
        calls_hist = defaultdict(int)
        for call in self.get_client_calls():
            calls_hist[round(call.wait_time, 2)] += 1
        return calls_hist


    def system_state_hist_calls(self):
        system_hist = {}
        hours = []
        people_in_system = []
        for call in self.calls:
            system_hist[call.arrival_time] = 1  # Mark arrival
            system_hist[call.arrival_time + datetime.timedelta(seconds=call.service_time + call.wait_time)] = 0  # Mark leave
        for i, system_event in enumerate(sorted(system_hist.items(), key=lambda x: x[0])):
            if i == 0:
                hours.append(system_event[0])
                people_in_system.append(1)
            else:
                people_in_system.append(people_in_system[i-1] + 1 if system_event[1] == 1 else people_in_system[i-1] - 1)
                hours.append(system_event[0])
        hours.append(hours[-1] + datetime.timedelta(seconds=1))
        return people_in_system, hours

    def system_state_hist_chats(self):
        system_hist = {}
        hours = []
        people_in_system = []
        for chat in self.chats:
            system_hist[chat.arrival_time] = 1  # Mark arrival
            system_hist[chat.arrival_time + datetime.timedelta(seconds=chat.service_time + chat.wait_time)] = 0  # Mark leave
        for i, system_event in enumerate(sorted(system_hist.items(), key=lambda x: x[0])):
            if i == 0:
                hours.append(system_event[0])
                people_in_system.append(1)
            else:
                people_in_system.append(people_in_system[i-1] + 1 if system_event[1] == 1 else people_in_system[i-1] - 1)
                hours.append(system_event[0])
        hours.append(hours[-1] + datetime.timedelta(seconds=1))
        return people_in_system, hours


