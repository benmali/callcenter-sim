from callcenter import CallQueue, ChatQueue, CustomerServiceAgent


class CallCenter:
    def __init__(self, service_agents: set):
        self.service_agents = service_agents
        self.call_queue = CallQueue()
        self.chat_queue = ChatQueue()

    def end_agent_shift(self, agent: CustomerServiceAgent):
        """
        Remove an agent from shift
        """
        self.service_agents.remove(agent)

    def start_agent_shift(self, agent: CustomerServiceAgent):
        """
        Add an agent to shift
        """
        self.service_agents.add(agent)
