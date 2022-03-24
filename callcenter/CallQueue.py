class CallQueue:
    def __init__(self, mode='PriorityQueue'):
        if mode == 'PriorityQueue':
            # We seperate to 2 queues in a priority queue mode
            # Where restauranuts are pulled frirst from the queue
            self.clients = []
            self.restaurants = []
        elif mode == 'SeparatePool':
            pass
            # Service agents are divided to 2 teams
            # One for restaraunts, one for clients - we expect to see restaurants idle a lot while other queue crashes
        else:
            # Current state, one pool, no priority
            self.queue = []