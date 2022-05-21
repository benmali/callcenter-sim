from callcenter import CallQueue, ChatQueue, CustomerServiceAgent, Metrics, Event, Graphs
import math
import callcenter
from helpers import Probabilities, TimeHelper
import numpy as np
import heapq as hpq
import datetime
import logging
import sys
import json

logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
    stream=sys.stdout
)

logger = logging.getLogger('CallCenter')


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
# We assume that as long as the restaurant queue isn't empty, the call rate and chat rate raises by 1.1^ len(rest_queue)

# TODO - Add queue metrics (average lengths - histogram)
# TODO - Add interface to change the distributions
# TODO - Test different modes
# TODO - add restaurant calling


class CallCenter:
    def __init__(self, mode: str = "PriorityQueue"):
        self.events = []
        self.metrics_list = []
        self.day_metrics = None
        self.user_parameters = self._read_user_parameters()
        sim_mode = self.user_parameters.get("Simulation Mode")
        sim_map = {'Regular': 'Regular', "Separate Queues": "SeparatePool", "Priority Queue": "PriorityQueue"}
        self.mode = sim_map[sim_mode]  # PriorityQueue, SeparatePool, Regular
        self.n_high_tech_employees = int(self.user_parameters.get("High-Tech Employees"))
        self.n_industry_employees = int(self.user_parameters.get("Industry Employees"))
        self.curr_time = TimeHelper.string__to_full_time('01-01-2021 08:00:00')
        self.opening_hour = TimeHelper.string_to_hour('08:00:00')
        self.closing_hour = TimeHelper.string_to_hour('23:00:00')
        self.n_restaurants = 1_000
        self.call_queue = CallQueue(self.mode)
        self.chat_queue = ChatQueue(self.mode)
        self.n_rest_in_queue = 0
        self.rest_call_proportion = 0.03  # 3% of all calls belong to restaurants
        self.weather = self.user_parameters.get("Weather").lower()
        self.n_chat_agents = int(self.user_parameters.get("Number of Chat Agents"))
        self.n_call_agents = int(self.user_parameters.get("Number of Call Agents"))
        self.starting_number_of_agents = self.n_chat_agents + self.n_call_agents
        Probabilities.client_patience_ex = float(self.user_parameters.get("Client Patience ~ E(X)"))
        Probabilities.client_patience_var = float(self.user_parameters.get("Client Patience ~ V(X)"))
        Probabilities.rain_factor = float(self.user_parameters.get("Rain Factor"))
        Probabilities.holiday = self.user_parameters.get("Holiday")
        if self.mode == 'SeparatePool':
            percentage_of_rest_agents = 0.2  # 20% of the agents will answer calls from restaurants
            self.n_rest_agents = math.ceil(
                self.starting_number_of_agents * percentage_of_rest_agents)  # At least 1 agent
            self.n_end_client_agents = self.starting_number_of_agents - self.n_rest_agents  # Other agents serve clients
            # i % 2 condition splits half the agents for chat duty other half for calls
            self.end_service_agents = [
                CustomerServiceAgent(i, self.call_queue if i % 2 == 0 else self.chat_queue, self.curr_time) for i in
                range(self.n_end_client_agents)]
            self.rest_service_agents = [CustomerServiceAgent(i, self.call_queue, self.curr_time) for i in
                                        range(self.n_rest_agents)]
        else:  # Regular and PriorityQueue
            # i % 2 condition splits half the agents for chat duty other half for calls
            self.service_agents = [
                CustomerServiceAgent(i, self.call_queue if i % 2 == 0 else self.chat_queue, self.curr_time) for i in
                range(self.starting_number_of_agents)]

        self.n_end_clients = 100_0000
        self.n_employees_by_sector = {"High-Tech": 800_000,
                                      "Blue-Collar": 200_000}  # Map the number of employees by sector
        self.companies = []  # This list only grows along iteration
        self.event_mapping = {
            'incoming_call_or_chat': self.incoming_call_or_chat,
            'end_call_or_chat': self.end_call_or_chat,
            'sign_new_company': self.sign_new_company,
            'sign_new_restaurant': self.sign_new_restaurant,
            'end_agent_break': self.end_agent_break,
            'restaurant_end_ingredient': self.rest_end_ingredient
        }
        self.queue_map = {"call": self.call_queue, "chat": self.chat_queue}

    def incoming_call_or_chat(self, event):
        """
        arriving call/chat message
        :param event: Event object
        :return:
        """

        client = event.client
        if client.client_type == 'Restaurant':
            self.n_rest_in_queue += 1
        client.arrival_time = self.curr_time
        self.day_metrics.arrival_histogram[self.curr_time.hour] += 1  # arrival histogram is default dict
        logger.info(f"Incoming {event.client.contact_method} from {client}")
        if event.client.contact_method == 'call':
            self.call_queue.enqueue(client)
        else:
            self.chat_queue.enqueue(client)

        # If an agent is available, call end_call event
        if self.mode == 'SeparatePool':
            if client.client_type == 'Restaurant':
                agents = self.rest_service_agents
                queue = 'restaurants'
            else:
                agents = self.end_service_agents
                queue = 'clients'

        else:
            agents = self.service_agents
            queue = None

        # Try pulling from queue directly on incoming call, at least one call or chat in queue
        queue_to_pull = self.decide_call_or_chat()
        curr_client = None  # No client is pulled yet
        for agent in agents:
            if queue_to_pull == 'call':
                if agent.is_free_for_call():
                    curr_client = self.dequeue_call(queue)
            else:
                if agent.is_free_for_chat():
                    curr_client = self.dequeue_chat(queue)

            # An agent is free to take a client call or chat
            if curr_client:
                logger.info(f"{agent} answering {client.contact_method} at {self.curr_time}")
                contact_duration = agent.handle_client(curr_client)
                client.set_wait_time(self.curr_time)
                client.set_service_time(contact_duration)  # Update call duration
                hpq.heappush(self.events,
                             callcenter.Event(self.curr_time + datetime.timedelta(seconds=contact_duration),
                                              'end_call_or_chat',
                                              curr_client, agent))  # Push new arrival
                break

        # # Generate new chats and call arrivals
        next_contact_time = self.curr_time + datetime.timedelta(hours=Probabilities.contact_rate(self.curr_time,
                                                                                           self.n_rest_in_queue,
                                                                                           self.n_high_tech_employees,
                                                                                           self.n_industry_employees,
                                                                                           self.weather))

        if np.random.uniform(0, 1) < 0.03:  # 3% are rests
            hpq.heappush(self.events,
                         callcenter.Event(next_contact_time, 'incoming_call_or_chat',
                                          callcenter.Client(next_contact_time, 'Restaurant')))  # Push new rest arrival
        else:
            hpq.heappush(self.events,
                         callcenter.Event(next_contact_time, 'incoming_call_or_chat',
                                          callcenter.Client(next_contact_time)))  # Push new arrival

    def end_call_or_chat(self, event):
        """
        End call or chat for agent
        @param event:
        @return:
        """
        agent = event.agent
        client = event.client
        client_data = client.get_metrics()
        if client.client_type == 'Restaurant':
            self.n_rest_in_queue -= 1
        self.day_metrics.add_call_or_chat(client_data)
        break_time = agent.end_call_or_chat()
        logger.debug(
            f"{agent} - break? {break_time} at {self.curr_time}. ending {agent.task_assigned} - duration: {client_data.service_time / 60 }")
        if break_time:
            logger.debug(f"Agent {agent} is going for a break for {break_time // 60} minutes at {self.curr_time}")
            hpq.heappush(self.events,
                         callcenter.Event(self.curr_time + datetime.timedelta(seconds=break_time), 'end_agent_break',
                                          None, agent))  # Push new arrival

        # Agent is not going for a break
        else:
            queue = agent.task_assigned  # assigned to call or chat
            pulled_valid_client = False
            while not self.queue_map[queue].is_empty():  # Pull another client if queue isn't empty
                logger.debug(f"{agent} {agent.task_assigned} end - trying to pull another client {self.curr_time}")
                client = self.queue_map[queue].dequeue(queue)
                if self.curr_time - client.arrival_time > client.max_wait_time:
                    client.abandon_queue()
                    client_data = client.get_metrics()
                    logger.info(f"{client} abandoned at {client.abandon_time}")
                    self.day_metrics.add_abandonment(client_data)
                    continue
                pulled_valid_client = True
                logger.debug(f"{agent} {agent.task_assigned} pulled another client {self.curr_time}")
                contact_duration = agent.handle_client(client)
                client.update_metrics(self.curr_time, contact_duration)
                hpq.heappush(self.events,
                             callcenter.Event(self.curr_time + datetime.timedelta(seconds=contact_duration),
                                              'end_call_or_chat',
                                              client, agent))  # Push new arrival
                break

            if not pulled_valid_client:
                logger.debug(f"{agent} empty queue at {self.curr_time}")
            # No calls to pull, set agent as free

    def end_agent_break(self, event) -> None:
        """
        Return agent from break event
        @param event: event
        @return: None
        """
        agent = event.agent
        logger.debug(f"{agent} returned from a break at {self.curr_time}")
        agent.return_from_break()
        queue = agent.task_assigned  # assigned to call or chat
        if not self.queue_map[queue].is_empty():  # Pull another client if queue isn't empty
            client = self.queue_map[queue].dequeue(queue)
            contact_duration = agent.handle_client(client)
            logger.info(f"{agent} answering {client.contact_method} at {self.curr_time}")
            client.update_metrics(self.curr_time, contact_duration)
            hpq.heappush(self.events,
                         callcenter.Event(self.curr_time + datetime.timedelta(seconds=contact_duration),
                                          'end_call_or_chat',
                                          client, agent))  # Push new arrival
        else:
            logger.debug(f"{agent} returned from a break and queue is empty")

    def _read_user_parameters(self) -> dict:
        """
        Read the parameters JSON the user created and use the paramters in the simulation with them
        @return: dict
        """
        try:
            with open("../callcenter/user_parameters.json") as f:
                user_params = json.load(f)
            return user_params
        except Exception as e:
            logger.exception(e)
            return {}

    def rest_end_ingredient(self, event):
        """
        Simulate a restaurant running out of something
        The restaurant keeps getting orders for some dish they cant make
        Clients order this and their food wont arrive
        @return:
        """
        pass
        # Generate next restaurant call
        rest = callcenter.Client(self.curr_time, 'Restaurant')
        hpq.heappush(self.events,
                     callcenter.Event(self.curr_time, 'incoming_call_or_chat', rest))  # Push new arrival
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
        print(next_rest_sign_date)
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

    def decide_call_or_chat(self):
        """
        Decide which queue to try and answer
        This probability gives 50-50 ratio to try and answer call and chats at the same rate
        @return:
        """
        probability = np.random.uniform(0, 1)
        preferred_queue = 'call' if probability < 0.4 else 'chat'
        if preferred_queue == 'call':
            if not self.call_queue.is_empty():
                return 'call'
            else:
                return 'chat'
        elif preferred_queue == 'chat':
            if not self.chat_queue.is_empty():
                return 'chat'
            else:
                return 'call'

    def run(self):
        for i in range(1):  # Iterate over a year of events
            np.random.seed(i + 1)
            # self.sign_new_company()
            client = callcenter.Client(self.curr_time)
            self.day_metrics = Metrics(self.curr_time)
            hpq.heappush(self.events, callcenter.Event(client.arrival_time, "incoming_call_or_chat", client))
            while self.curr_time.hour < self.closing_hour.hour:
                event = hpq.heappop(self.events)
                self.curr_time = event.time
                handle_event = self.event_mapping.get(event.event_type)
                handle_event(event)
            print("\n------ Metrics ------\n")
            print(f"Chat abandon {self.day_metrics.chat_client_abandoned}")
            print(f"Call abandon {self.day_metrics.call_client_abandoned}")
            print(f"Arrival histogram for {self.curr_time.date()}: {dict(self.day_metrics.arrival_histogram)}")
            print(f"Number of chats handled {len(self.day_metrics.chats)}")
            print(f"Number of calls handled {len(self.day_metrics.calls)}")
            print(f"Call reason breakdown: {self.day_metrics.get_contact_reason_breakdown('call')}")
            print(f"Chat reason breakdown: {self.day_metrics.get_contact_reason_breakdown('chat')}")
            Graphs.plot_call_abandon_times(self.day_metrics.get_call_abandonments())
            Graphs.plot_arrival_histogram(self.day_metrics.arrival_histogram)
            Graphs.plot_rest_wait_histogram(self.day_metrics.get_rest_wait_histogram())
            Graphs.plot_system_hist_chats(*self.day_metrics.system_state_hist_chats())
            Graphs.plot_client_wait_histogram(self.day_metrics.get_client_call_wait_histogram())
            Graphs.plot_system_hist_calls(*self.day_metrics.system_state_hist_calls())  # must be last to display results correctly
            # reset day
            self.events = []
            self.curr_time = TimeHelper.set_next_day(self.curr_time)


if __name__ == "__main__":
    cc = CallCenter()
    cc.run()
