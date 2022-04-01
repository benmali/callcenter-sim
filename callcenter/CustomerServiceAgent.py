from helpers import Probabilities

from callcenter import Event


class CustomerServiceAgent:
    def __init__(self, agent_id):
        self.seniority = 0
        self.agent_id = agent_id
        self.calls = []
        self.chats = []
        self.on_break = False
        self.office_duty_break = False
        self.is_free = False
        self.n_short_breaks = 0  # Allowed number of breaks is 3 breaks of up to 3 min
        self.n_long_breaks = 0  # Allowed number of breaks is 1 break of up to 10 min
        self.lunch_break = 0  # Allowed number of breaks is 1 break of up to 45 min

    def __hash__(self):
        """
        Use this to store agents in a set
        Assume unique IDs
        """
        return hash(self.agent_id)

    def go_to_break(self):
        self.is_free = False
        self.on_break = True

    def go_to_office_break(self):
        self.is_free = False
        self.office_duty_break = True

    def return_from_break(self):
        self.is_free = True
        self.on_break = False
        self.office_duty_break = False

    def answer_call(self, client):
        self.is_free = False
        call_time = Probabilities.call_duration(client)
        return call_time
        # Calculate call time (randomize)
        # Push to heap being free

    def end_call(self):
        self.is_free = True
        # Probability to take a break
        # Push to heap being free

    def answer_chat(self, client):
        self.is_free = False
        chat_time = Probabilities.chat_duration(client)
        return chat_time
        # Push to heap being free
