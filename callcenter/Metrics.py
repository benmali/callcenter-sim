import datetime


class Metrics:
    def __init__(self, metric_date: datetime.datetime):
        self.metric_date = metric_date
        self.total_calls = 0
        self.total_chats = 0
        self.calls = [] # Store whole tuple of data
        self.chats = [] # Store whole tuple of data
        self.chat_durations = []
        self.call_durations = []
        self.number_of_calls = 0
        self.number_of_chats = 0
        self.call_wait_times = []
        self.chat_wait_times = []  # call_id: (enter time+date, duration waited)
        self.n_rejected_calls = 0  #
        self.agent_starvation = {}  # time agent had no work (waited for work)
        self.queue_lengths = {}  # Time: (len(call_queue), len(chat_queue)
    # Number of end employees ratio to agents
    # What is the number of agents needed to provide SLA when a new company of size X signs?

    def add_call_or_chat(self, client_data):
        contact_method = client_data.contact_method
        if contact_method == "call":
            self.calls.append(client_data)
            # add other stuff here
        else:
            self.chats.append(client_data)


