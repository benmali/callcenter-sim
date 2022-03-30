from callcenter import CallQueue, ChatQueue, CustomerServiceAgent


class CallCenter:
    def __init__(self, mode: str, number_of_agents: int = 10):
        self.starting_number_of_agents = number_of_agents
        self.service_agents = [CustomerServiceAgent(i) for i in range(self.starting_number_of_agents)]
        self.call_queue = CallQueue(mode)
        self.chat_queue = ChatQueue(mode)

    def end_agent_shift(self, agent: CustomerServiceAgent):
        """
        Remove an agent from shift
        """
        self.service_agents.remove(agent)

    def start_agent_shift(self, agent: CustomerServiceAgent):
        """
        Add an agent to shift
        """
        self.service_agents.append(agent)

    def enqueue_call(self, client,  mode: str) -> None:
        """
        Add call to queue depending on the mode
        @param mode:
        @return:
        """
        self.call_queue.enqueue(client)

    def enqueue_chat(self,client,  mode: str) -> None:
        """
        Add chat to queue depending on the mode
        @param mode:
        @return:
        """
        pass