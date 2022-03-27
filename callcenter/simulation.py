import numpy as np
import heapq as hpq
import callcenter
from helpers import Probabilities


class CallCenterSimulation:
    def __init__(self):
        self.events = []
        self.common_pool_scenario_no_pq = True  # Common pool without priority queue for restaurants
        self.common_pool_pq = False  # Common pool with priority queue for restaurants
        self.separated_pools = False  # Pool for restaurants and pool for clients
        self.metrics = callcenter.Metrics()
        self.n_end_clients = 1000
        self.n_employees_by_sector = {"High-Tech": 0, "Blue-Collar": 0}  # Map the number of employees by sector
        self.companies = []  # This list only grows along iteration
        self.mode = "PriorityQueue"
        # The day type (rainy w/e) is in charge of where is my food calls/chat
        # Sector and age are in charge of reset my password/ login issues/ cant process my order cause of rules

        # Assumptions - Where is my food call number rises on rainy days -> and are direct derivitive of total number of end clients
        # Login/password/order process calls are unrelated to weather (no correlation)

    def incoming_call(self, event):
        """
        arriving call/chat message
        :param event: Event object
        :return:
        """
        client = event.client
        current_floor = client.current_floor  # current floor number, use as index to access floor list
        # search for elevator in this floor

        hpq.heappush(self.events, callcenter.Event(client.arrival_time, callcenter.Client))

    def incoming_chat(self):
        # Randomize handling time, push to event finish chat
        # Add to Metrics handling time
        pass

    def sign_new_company(self):
        n_employees, sector = Probabilities.company_size_and_sector_distribution()

        self.n_end_clients += 1
        # Generate random number of employees, sector and number of employees
        # Add the number of new employees to total pool

    def sign_new_restaurant(self):
        pass

    def agent_break(self):
        pass
        # Which agent
        # Randomize break time, push return to event list

    def run(self):

        for i in range(365):  # Iterate over a year of events
            np.random.seed(i+1)
            client = self.gen_client()
            hpq.heappush(self.events, Event(client.arrival_time, "arriving", None, None, client))
            if self.saturday:
                for elevator in self.elevators:
                    hpq.heappush(self.events, Event(self.curr_time, "door open", elevator.floor, elevator.number))
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




