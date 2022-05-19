

class Queue:
    def __init__(self, mode='PriorityQueue'):
        self.mode = mode
        self.clients = []
        self.restaurants = []
        self.queue_map = {'clients': self.clients,
                          'restaurants': self.restaurants}

    def is_empty(self, queue=None) -> bool:
        """
        Assert is queue is empty
        @return: bool
        """
        if queue == "clients":
            return len(self.clients) == 0

        elif queue == "restaurants":
            return len(self.restaurants) == 0

        return len(self.clients) == 0 and len(self.restaurants) == 0

    def _pull_priority(self):
        """
        Pull method for priority queue
        """
        if self.restaurants:  # Queue not empty
            client = self.restaurants.pop(0)  # Pull first restaurant from the queue and remove from list
        else:
            client = self.clients.pop(0)
        return client

    def _pull_separate(self, queue: str):
        """
        Pull method for separated pools
        @param: queue - name of the queue
        """
        if not queue:
            raise ValueError("Queue must be specified when using Separate Pools mode")
        client = self.queue_map[queue].pop(0)  # Pull from specified queue
        return client

    def _pull_queue(self):
        """
        Pull method
        """
        return self.clients.pop(0)

    def dequeue(self, queue=None):
        """
        Pull a new chat
        Pull only triggers when queue is greater than 0
        """
        try:
            if self.mode == 'PriorityQueue':
                return self._pull_priority()

            elif self.mode == 'SeparatePool':
                return self._pull_separate(queue)
            else:
                return self._pull_queue()

        except IndexError as e:
            print("Tried pulling from an empty client list")
            raise e

        except Exception as e:
            print(e)

    def enqueue(self, client):
        """
        Client can be restaurant as well
        """
        if self.mode in ('PriorityQueue', 'SeparatePool'):
            if client.client_type == 'Restaurant':
                self.restaurants.append(client)
            else:
                self.clients.append(client)
        else:
            self.clients.append(client)

