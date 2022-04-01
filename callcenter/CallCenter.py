from callcenter import CallQueue, ChatQueue, CustomerServiceAgent, Metrics, Event, Restaurant
import math
import callcenter
from helpers import Probabilities, TimeHelper
import numpy as np
import heapq as hpq


# Call duration is dependent on client not agent

class CallCenter:
    def __init__(self, mode: str, number_of_agents: int = 10):

        self.events = []
        self.curr_date = TimeHelper.string_to_date('01-01-2021')
        self.curr_hour = '08:00'
        self.closing_hour = '20:00'
        self.curr_time = None  # This needs to be the curr time and the curr date
        self.mode = "PriorityQueue"
        self.common_pool_scenario_no_pq = True  # Common pool without priority queue for restaurants
        self.common_pool_pq = False  # Common pool with priority queue for restaurants
        self.separated_pools = False  # Pool for restaurants and pool for clients
        self.n_end_clients = 1000
        self.n_employees_by_sector = {"High-Tech": 0, "Blue-Collar": 0}  # Map the number of employees by sector
        self.companies = []  # This list only grows along iteration
        self.event_mapping = {
            'incoming_call': self.incoming_call,
            'end_call': self.end_call,
            'end_chat': self.end_chat,
            'sign_new_company': self.sign_new_company,
            'sign_new_restaurant': self.sign_new_restaurant,
            'agent_break': self.agent_break
        }

    def incoming_call(self, event):
        """
        arriving call/chat message
        :param event: Event object
        :return:
        """
        client = event.client
        self.enqueue_call(client)
        next_call_time = client.arrival_time + Probabilities.call_rate(client.arrival_time)
        hpq.heappush(self.events,
                     callcenter.Event(next_call_time, 'incoming_call', callcenter.Client))  # Push new arrival

    def incoming_chat(self, event):
        # Randomize handling time, push to event finish chat
        # Add to Metrics handling time
        client = event.client
        client.arrival_time = self.curr_time
        self.enqueue_chat(client)
        next_chat_time = client.arrival_time + Probabilities.chat_rate(client.arrival_time)
        # if agent is available, set agent busy > push end call to queue
        # if no agent is available, add call to queue
        hpq.heappush(self.events,
                     callcenter.Event(next_chat_time, 'incoming_call', callcenter.Client))  # Push new arrival

    def end_call(self, event):
        agent = event.agent
        agent.end_call()
        # Pull another call/chat
        # Set agent as free
        # In some probability agent takes a break - not more than 3 bathroom breaks (3min) 1 longer - (10min) 1 for (50min)

    def end_chat(self, event):
        agent = event.agent
        agent.end_chat()
        pass

    # Pull another call/chat

    def sign_new_company(self):
        """
        Handle new company sign event
        @return:
        """
        n_employees, sector = Probabilities.company_size_and_sector_distribution()

        self.n_end_clients += 1
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

    def agent_break(self):
        pass
        # Which agent
        # Randomize break time, push return to event list

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

        if self.mode == 'SeparatePool':
            percentage_of_rest_agents = 0.2  # 20% of the agents will answer calls from restaurants
            self.n_rest_agents = math.ceil(self.starting_number_of_agents * percentage_of_rest_agents)  # At least 1 agent
            self.n_end_client_agents = self.starting_number_of_agents - self.n_rest_agents  # Other agents serve clients
            self.end_service_agents = [CustomerServiceAgent(i) for i in range(self.n_end_client_agents)]
            self.rest_service_agents = [CustomerServiceAgent(i) for i in range(self.n_rest_agents)]
        else:
            self.service_agents = [CustomerServiceAgent(i) for i in range(self.starting_number_of_agents)]

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

    def dequeue_call(self, agent, queue=None):
        if not queue:
            client = self.call_queue.dequeue()
            client.wait_time = self.curr_time - client.arrival_time  # Calc time for client in queue
        else:
            client = self.call_queue.dequeue(queue)
        call_time = Probabilities.call_duration(client)
        return Event(self.curr_time + call_time, 'end_call', client, agent)

    def enqueue_call(self, client) -> None:
        """
        Add call to queue depending on the mode
        @param client:
        @return:
        """
        self.call_queue.enqueue(client)
        if self.mode == 'SeparatePool':
            if isinstance(client, Restaurant):
                agents = self.rest_service_agents
                queue = 'restaurants'
            else:
                agents = self.end_service_agents
                queue = 'clients'

            for agent in agents:
                if agent.is_free:
                    # Assign call to agent
                    agent.is_free = False
                    self.dequeue_call(agent, queue)
        else:
            for agent in self.service_agents:
                if agent.is_free:
                    # Assign call to agent
                    agent.is_free = False
                    self.dequeue_call(agent)

    def enqueue_chat(self, client) -> None:
        """
        Add chat to queue depending on the mode
        @param client:
        @return:
        """
        self.chat_queue.enqueue(client)

