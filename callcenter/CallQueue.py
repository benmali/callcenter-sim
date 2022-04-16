from callcenter.ClientQueue import Queue


class CallQueue(Queue):
    def __init__(self, mode='PriorityQueue'):
        super().__init__(mode)
        self.queue_type = 'call'

