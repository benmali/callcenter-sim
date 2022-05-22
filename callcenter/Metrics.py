import datetime
from collections import defaultdict
from helpers import TimeHelper
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
        self.call_abandonments = []
        self.chat_abandonments = []
        self.arrival_histogram = defaultdict(int)
    # Number of end employees ratio to agents
    # What is the number of agents needed to provide SLA when a new company of size X signs?

    @staticmethod
    def _create_hours_strings(time: datetime.datetime):
        """
        Create a string of half hours to store data in dictionary by half hours
        @param time:
        @return:
        """
        return f"{time.hour}.{5 if time.minute // 30 > 0 else 0}"

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
            self.call_abandonments.append(client_data)
            # add other stuff here
        else:
            self.chat_client_abandoned += 1
            self.chat_abandonments.append(client_data)

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

    def get_call_abandonments(self):
        call_abandon_hist = defaultdict(int)
        for call in self.call_abandonments:
            if call.wait_time < 0:
                continue
            abandon_time = call.arrival_time + datetime.timedelta(minutes=call.wait_time)
            call_abandon_hist[self._create_hours_strings(abandon_time)] += 1
        return call_abandon_hist

    def get_chat_abandonments(self):
        chat_abandon_hist = defaultdict(int)

    def get_rest_calls(self):
        return [call for call in self.calls if call.client_type == 'Restaurant']

    def get_rest_wait_histogram(self):
        """
        Get number of rest waiting specific time
        @return:
        """
        rest_calls_hist = defaultdict(int)
        for call in self.get_rest_calls():
            if call.wait_time < 0:
                continue
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
            if call.wait_time < 0:
                continue
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
                if system_event[1] == 1:
                    people_in_system.append(people_in_system[i - 1] + 1)
                else:
                    if people_in_system[i-1] - 1 < 0:
                        people_in_system.append(0)
                    else:
                        people_in_system.append(people_in_system[i-1] - 1)
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


