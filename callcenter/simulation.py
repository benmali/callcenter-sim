import numpy as np
import heapq as hpq
import callcenter


class CallCenterSimulation:
    def __init__(self):
        self.events = []
        self.common_pool_scenario_no_pq = True  # Common pool without priority queue for restaurants
        self.common_pool_pq = False  # Common pool with priority queue for restaurants
        self.separated_pools = False  # Pool for restaurants and pool for clients

    def arriving(self, event):
        """
        arriving call/chat message
        :param event: Event object
        :return:
        """
        client = event.client
        current_floor = client.current_floor  # current floor number, use as index to access floor list
        # search for elevator in this floor
        if not self.saturday:
            for elevator in self.elevators:
                # there is an Elevator in the desired floor with closed doors, open doors
                if not elevator.start:
                    if elevator.floor == current_floor and not elevator.doors_open and client.desired_floor in elevator.service_floors:
                        elevator.start = True  # elevator won't open while moving
                        hpq.heappush(self.events,
                                     Event(client.arrival_time, "door open", current_floor, elevator.number))
                        break  # open just one Elevator
            if client.need_swap:  # add current and target floors to queue
                self.order_elevator(current_floor, "down", 0)
            else:  # client doesn't need swap
                direction = None  # if client arrived to a floor with an open elevator, do nothing
                if client.current_floor > client.desired_floor:
                    direction = "down"
                elif client.current_floor < client.desired_floor:
                    direction = "up"
                self.order_elevator(current_floor, direction, client.desired_floor)
        # don't do anything if it's Saturday elevators