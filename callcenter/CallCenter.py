import callcenter


class CallCenter:
    def __init__(self, service_agents: set):
        self.service_agents = service_agents
        self.call_queue = callcenter.CallQueue()
        self.chat_queue = callcenter.ChatQueue()

    def end_agent_shift(self, agent: callcenter.CustomerServiceAgent):
        """
        Remove an agent from shift
        """
        self.service_agents.remove(agent)

    def start_agent_shift(self, agent: callcenter.CustomerServiceAgent):
        """
        Add an agent to shift
        """
        self.service_agents.add(agent)
