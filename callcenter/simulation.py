import numpy as np
import heapq as hpq
import callcenter
from helpers import Probabilities
from helpers import TimeHelper


class CallCenterSimulation:
    def __init__(self):
        self.events = []
        self.curr_date = TimeHelper.string_to_date('01-01-2021')
        self.curr_hour = '08:00'
        self.curr_time = None  # This needs to be the curr time and the curr date
        self.mode = "PriorityQueue"
        self.call_center = callcenter.CallCenter(self.mode)
        self.common_pool_scenario_no_pq = True  # Common pool without priority queue for restaurants
        self.common_pool_pq = False  # Common pool with priority queue for restaurants
        self.separated_pools = False  # Pool for restaurants and pool for clients
        self.metrics = callcenter.Metrics()
        self.n_end_clients = 1000
        self.n_employees_by_sector = {"High-Tech": 0, "Blue-Collar": 0}  # Map the number of employees by sector
        self.companies = []  # This list only grows along iteration

        # The day type (rainy w/e) is in charge of where is my food calls/chat
        # Sector and age are in charge of reset my password/ login issues/ cant process my order cause of rules

        # Assumptions - Where is my food call number rises on rainy days -> and are direct derivitive of total number of end clients
        # Assumption - companies never leave the service
        # Assumption call duration for blue collar will be longer
        # Login/password/order process calls are unrelated to weather (no correlation)

    def incoming_call(self, event):
        """
        arriving call/chat message
        :param event: Event object
        :return:
        """
        client = event.client
        hpq.heappush(self.events, callcenter.Event(client.arrival_time, 'incoming_call', callcenter.Client))  # Push new arrival
        hpq.heappush(self.events, callcenter.Event(client.arrival_time, 'end_call', callcenter.Client))  # Push call end

    def incoming_chat(self, event):
        # Randomize handling time, push to event finish chat
        # Add to Metrics handling time
        pass
        client = event.client
        # if agent is available, set agent busy > push end call to queue
        # if no agent is available, add call to queue
        hpq.heappush(self.events, callcenter.Event(client.arrival_time, 'incoming_call', callcenter.Client))  # Push new arrival
        hpq.heappush(self.events, callcenter.Event(client.arrival_time, 'end_chat', callcenter.Client))  # Push chat end

    def end_call(self):
        pass
        # Set agent free
        # In some probability agent takes a break - not more than 3 bathroom breaks (3min) 1 longer - (10min) 1 for (50min)

    def end_chat(self):
        pass

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
            np.random.seed(i+1)
            self.sign_new_company()
            client = self.gen_client()
            hpq.heappush(self.events, callcenter.Event(client.arrival_time, "arriving", client))
            hpq.heappush(self.events, callcenter.Event(self.curr_time, "door open", client))
            while self.curr_time < self.simulation_time:
                event = hpq.heappop(self.events)
                self.curr_time = event.time
                if event.event_type == "arriving":
                    self.arriving(event)
                elif event.event_type == "door open":
                    self.door_open(event)
                elif event.event_type == "elevator fix":
                    self.elevator_fix(event)
                elif event.event_type == "door close":
                    self.door_close(event)
            for floor in self.floors:
                for client in floor.line:
                    if (self.curr_time - client.arrival_time) > 15 * 60 and not client.got_service:
                        self.abandoned += 1
            avg_cap = list(map(lambda x: x / (self.curr_time - 21600), self.elevators_avg_cap))
            self.abandoned_lst.append(self.abandoned)
            for key, value in self.service_dist.items():
                self.service_times[key] += value
            for j in range(len(avg_cap)):
                self.elevator_mat[i][j] = avg_cap[j]




