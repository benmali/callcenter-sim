import numpy as np
import callcenter


class Client:
    """
    A class to represent a client
    """

    def __init__(self, sector, age, call: callcenter.Call):
        self.sector = sector
        self.age = age
        self.wait_time = 0
        self.calls = []

    def __repr__(self):
        return f"Client's arrival time is"

    def add_wait_time(self, time):
        self.wait_time += time

    @classmethod
    def gen_client(cls):
        """
        generates Client object with arrival time, desired floor, and current floor
        :return: Client object
        """
        # initializing the arrival rates
        morning = [150, 400, 90, 84, 60, 120, 60, 36]
        afternoon = [90, 120, 150, 84, 60, 400, 60, 36]
        other = [60, 70, 60, 84, 60, 70, 60, 36]
        # creating morning/afternoon/other arrival probabilities
        m_prob = [morning[i] / 1000 for i in range(len(morning))]
        a_prob = [afternoon[i] / 1000 for i in range(len(afternoon))]
        o_prob = [other[i] / 500 for i in range(len(other))]
        rows_in_table = [i for i in range(8)]  # each row represents a row in the given arrival rates table
        # each tuple represents a cell in the given arrival rates table
        arrivals = [(0, 1), (0, 1), (1, 16), (1, 16), (1, 16), (16, 26), (16, 26), (16, 26)]
        # each tuple represents a cell in the given arrival rates table
        destinations = [(1, 16), (16, 26), (0, 1), (1, 16), (16, 26), (0, 1), (1, 16), (16, 26)]
        # matching the probabilities to time of simulation clock
        if self.curr_time >= 25200 and self.curr_time <= 36000:
            probs = m_prob
            time = 'morning'
        elif self.curr_time >= 54000 and self.curr_time <= 64800:
            probs = a_prob
            time = 'afternoon'
        else:
            probs = o_prob
            time = 'other'
        # generating a client curr_floor, desired_floor
        row = int(np.random.choice(rows_in_table, p=probs, size=1))
        curr_floor = arrivals[row]
        curr_floor = np.random.randint(curr_floor[0], curr_floor[1])
        desired_floor = destinations[row]
        desired_floor_tmp = np.random.randint(desired_floor[0], desired_floor[1])
        # if we created the client's desired floor as his arrival floor, choose another floor
        while curr_floor == desired_floor_tmp:
            desired_floor_tmp = np.random.randint(desired_floor[0], desired_floor[1])
        desired_floor = desired_floor_tmp
        # generate arrival time
        if time == 'morning':
            y = np.random.exponential(1 / (1000 / 3600))
        elif time == 'afternoon':
            y = np.random.exponential(1 / (1000 / 3600))
        else:
            y = np.random.exponential(1 / (500 / 3600))

        return cls(curr_floor, desired_floor, y + self.curr_time)