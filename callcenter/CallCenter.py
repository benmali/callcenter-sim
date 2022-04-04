from callcenter import CallQueue, ChatQueue, CustomerServiceAgent, Metrics, Event, Restaurant
import math
import callcenter
from helpers import Probabilities, TimeHelper
import numpy as np
import heapq as hpq


# ----- Assumptions -----
# Call duration is dependent on client not agent
# The day type (rainy w/e) is in charge of where is my food calls/chat
# Sector and age are in charge of reset my password/ login issues/ cant process my order cause of rules
# Where is my food call number rises on rainy days -> and are direct derivitive of total number of end clients
# companies never leave the service
# call duration for blue collar will be longer
# Login/password/order process calls are unrelated to weather (no correlation)
# Assuming restaurants only call (as most of them call anyway)
# Hofit said 60% is chat after the corona - so we will set this chance to generate a call or a chat


class CallCenter:
    def __init__(self, mode: str = "PriorityQueue", number_of_agents: int = 10):

        self.events = []
        self.curr_date = TimeHelper.string_to_date('01-01-2021')
        self.curr_hour = '08:00'
        self.curr_date_time = None
        self.closing_hour = '20:00'
        self.n_restaurants = 1_000
        self.curr_time = None  # This needs to be the curr time and the curr date
        self.mode = mode  # PriorityQueue, SeparatePool, Regular
        self.call_load_ratio = None  # queue size / number of agents assigned to calls
        self.chat_load_ratio = None  # queue size / number of agents assigned to chats
        self.starting_number_of_agents = number_of_agents
        self.call_queue = CallQueue(self.mode)
        self.chat_queue = ChatQueue(self.mode)

        if self.mode == 'SeparatePool':
            percentage_of_rest_agents = 0.2  # 20% of the agents will answer calls from restaurants
            self.n_rest_agents = math.ceil(
                self.starting_number_of_agents * percentage_of_rest_agents)  # At least 1 agent
            self.n_end_client_agents = self.starting_number_of_agents - self.n_rest_agents  # Other agents serve clients
            # i % 2 condition splits half the agents for chat duty other half for calls
            self.end_service_agents = [CustomerServiceAgent(i, i % 2 == 0) for i in range(self.n_end_client_agents)]
            self.rest_service_agents = [CustomerServiceAgent(i) for i in range(self.n_rest_agents)]
        else:
            # i % 2 condition splits half the agents for chat duty other half for calls
            self.service_agents = [CustomerServiceAgent(i, i % 2 == 0) for i in range(self.starting_number_of_agents)]

        self.n_end_clients = 100_0000
        self.n_employees_by_sector = {"High-Tech": 800_000,
                                      "Blue-Collar": 200_000}  # Map the number of employees by sector
        self.companies = []  # This list only grows along iteration
        self.event_mapping = {
            'incoming_call_or_chat': self.incoming_call_or_chat,
            'end_call': self.end_call,
            'end_chat': self.end_chat,
            'sign_new_company': self.sign_new_company,
            'sign_new_restaurant': self.sign_new_restaurant,
        }

    def incoming_call_or_chat(self, event):
        """
        arriving call/chat message
        :param event: Event object
        :return:
        """
        client = event.client
        client.arrival_time = self.curr_time

        if event.client.contact_method == 'call':
            self.call_queue.enqueue(client)
        else:
            self.chat_queue.enqueue(client)

        # If an agent is available, call end_call event
        if self.mode == 'SeparatePool':
            if isinstance(client, Restaurant):
                agents = self.rest_service_agents
                queue = 'restaurants'
            else:
                agents = self.end_service_agents
                queue = 'clients'

        else:
            agents = self.service_agents
            queue = None

        queue_to_pull = CallCenter.decide_call_or_chat()
        if queue_to_pull == 'call':
            for agent in agents:
                if agent.is_free_for_call():
                    client = self.dequeue_call(queue)
                    agent.answer_call(client)
                    call_duration = Probabilities.call_duration(client)
                    client.service_time = call_duration  # Update call duration
                    hpq.heappush(self.events,
                                 callcenter.Event(self.curr_time + call_duration,
                                                  'end_call_or_chat',
                                                  client, agent))  # Push new arrival
        else:
            for agent in agents:
                if agent.is_free_for_chat():
                    client = self.dequeue_chat(queue)
                    agent.answer_chat(client)
                    chat_duration = Probabilities.chat_duration(client)
                    client.service_time = chat_duration  # Update chat duration
                    hpq.heappush(self.events,
                                 callcenter.Event(self.curr_time + chat_duration,
                                                  'end_call_or_chat',
                                                  client, agent))  # Push new arrival

        # Generate new chats and call arrivals
        next_call_time = client.arrival_time + Probabilities.call_rate(client.arrival_time)
        hpq.heappush(self.events,
                     callcenter.Event(next_call_time, 'incoming_call_or_chat', callcenter.Client()))  # Push new arrival

        next_chat_time = client.arrival_time + Probabilities.chat_rate(client.arrival_time)
        hpq.heappush(self.events,
                     callcenter.Event(next_chat_time, 'incoming_call_or_chat', callcenter.Client()))  # Push new arrival

    def end_call_or_chat(self, event):
        agent = event.agent
        break_time = agent.end_call_or_chat()
        if break_time:
            hpq.heappush(self.events,
                         callcenter.Event(self.curr_time + break_time, 'end_agent_break',
                                          None, agent))  # Push new arrival

    def end_agent_break(self, event):
        agent = event.agent
        agent.return_from_break()


    def rest_end_ingredient(self):
        """
        Simulate a restaurant running out of something
        The restauarant keeps getting orders for some dish they cant make
        Clients order this and their food wont arrive
        @return:
        """
        pass
        # Simulate a call from a restaurant
        # This issue makes a lot of calls and complaints
        # To simplify, we will generate 5 client calls and 1 rest call for this event

    def sign_new_company(self):
        """
        Handle new company sign event
        @return:
        """
        n_employees, sector = Probabilities.company_size_and_sector_distribution()

        self.n_end_clients += n_employees
        self.n_employees_by_sector[sector] += n_employees

        # Generate random number of employees, sector and number of employees
        # Add the number of new employees to total pool
        next_company_sign_date = TimeHelper.add_days(self.curr_date, Probabilities.company_sign_rate())
        hpq.heappush(self.events, callcenter.Event(next_company_sign_date, 'sign_new_company'))  # Push chat end

    def sign_new_restaurant(self):
        """
        Handle new restaurant sign event
        @return:
        """

        next_rest_sign_date = TimeHelper.add_days(self.curr_date, Probabilities.restaurant_sign_rate())
        hpq.heappush(self.events, callcenter.Event(next_rest_sign_date, 'sign_new_restaurant'))  # Push chat end

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

    def dequeue_call(self, queue=None):
        if not queue:
            client = self.call_queue.dequeue()
            client.wait_time = self.curr_time - client.arrival_time  # Calc time for client in queue
        else:
            client = self.call_queue.dequeue(queue)
        return client

    def dequeue_chat(self, queue=None):
        if not queue:
            client = self.chat_queue.dequeue()
            client.wait_time = self.curr_time - client.arrival_time  # Calc time for client in queue
        else:
            client = self.chat_queue.dequeue(queue)
        return client

    def enqueue_chat(self, client) -> None:
        """
        Add chat to queue depending on the mode
        @param client:
        @return:
        """
        self.chat_queue.enqueue(client)

    @staticmethod
    def decide_call_or_chat():
        """
        Decide which queue to try and answer
        This probability gives 50-50 ratio to try and answer call and chats at the same rate
        @return:
        """
        probability = np.random.uniform(0, 1)
        return 'call' if probability < 0.5 else 'chat'

    def run(self):

        for i in range(365):  # Iterate over a year of events
            np.random.seed(i + 1)
            self.sign_new_company()
            client = self.gen_client()
            hpq.heappush(self.events, callcenter.Event(client.arrival_time, "incoming_call", client))

            while self.curr_hour < self.closing_hour:
                event = hpq.heappop(self.events)
                self.curr_time = event.time
                handle_event = self.event_mapping.get(event.event_type)
                handle_event(event)

        self.simulation = callcenter.CallCenterSimulation
        self.metrics = Metrics()  # Metrics to measure the call center performance
        self.mode = mode
        self.starting_number_of_agents = number_of_agents
        self.call_queue = CallQueue(self.mode)
        self.chat_queue = ChatQueue(self.mode)


if __name__ == "__main__":
    pass
