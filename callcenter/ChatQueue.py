from callcenter.Queue import Queue


class ChatQueue(Queue):
    def __init__(self, mode='PriorityQueue'):
        super().__init__(mode)


cq = ChatQueue()
print(cq.clients)
