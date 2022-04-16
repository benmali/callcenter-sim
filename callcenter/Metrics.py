class Metrics:
    def __init__(self):
        self.total_calls = 0
        self.total_chats = 0
        self.call_durations = {}
        self.chat_durations = {}
        self.call_wait_times = {}
        self.chat_wait_times = {}  # call_id: (enter time+date, duration waited)
        self.n_rejected_calls = {}  #
        self.agent_starvation = {}  # time agent had no work (waited for work)
    # Number of end employees ratio to agents
    # What is the number of agents needed to provide SLA when a new company of size X signs?


