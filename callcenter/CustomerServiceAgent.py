class CustomerServiceAgent:
    def __init__(self, agent_id):
        self.seniority = 0
        self.agent_id = agent_id
        self.calls = []
        self.chats = []
        self.on_break = False
        self.office_duty_break = False
        self.is_free = False

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

    def answer_call(self):
        pass
        self.is_free = False
        # Pull call from queue
        # Calculate call time (randomize)
        # Push to heap being free

    def answer_chat(self):
        pass
        self.is_free = False
        # Pull chat from queue
        # Calculate chat time (randomize)
        # Push to heap being free
