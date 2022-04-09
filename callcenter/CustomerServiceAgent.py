from helpers import Probabilities


class CustomerServiceAgent:
    def __init__(self, agent_id, task_assigned='call'):
        self.seniority = 0
        self.agent_id = agent_id
        self.call = 0  # Holds the number of calls the agent is executing, maximum of 1 call
        self.chats = 0  # Holds the number of calls the agent is executing, maximum of 1 call
        self.max_simultaneous_chats = 3
        self.max_simultaneous_calls = 1
        self.on_break = False
        self.office_duty_break = False
        self.task_assigned = task_assigned
        self.is_free = True
        self.wants_break = False  # Flag to stop routing calls or chats to agent
        self.n_short_breaks = 0  # Allowed number of breaks is 3 breaks of up to 3 min
        self.n_long_breaks = 0  # Allowed number of breaks is 1 break of up to 10 min
        self.max_short_breaks = 3
        self.max_long_breaks = 1
        self.lunch_break = 0  # Allowed number of breaks is 1 break of up to 45 min

    def __repr__(self):
        return f"Agent {self.agent_id}-task {self.task_assigned} free? {self.is_free}"

    def __hash__(self):
        """
        Use this to store agents in a set
        Assume unique IDs
        """
        return hash(self.agent_id)

    def set_for_break(self):
        """
        Stop routing calls or chats to this agent, as he/she wants to take a break
        @return:
        """
        self.wants_break = True

    def go_to_break(self):
        self.is_free = False
        self.on_break = True

    def go_to_office_break(self):
        self.is_free = False
        self.office_duty_break = True

    def return_from_break(self):
        self.is_free = True
        self.on_break = False
        self.office_duty_break = False

    def set_move_to_calls(self):
        """
        Makes agent finish his chats and assign him to calls
        @return:
        """

    def is_free_for_chat(self):
        """
        Check if agent can take a chat request
        Must be assigned for chat and have less than 4 chats
        Also, check that agent is free and not on any break or needs to go for a break of any kind
        @return:
        """
        return self.task_assigned == 'chat' and self.chats < self.max_simultaneous_chats and self.is_free and not self.wants_break

    def is_free_for_call(self):
        """
        Check if agent can take a chat request
        Must be assigned for calls and have less than 1 call
        Also, check that agent is free and not on any break or needs to go for a break of any kind
        @return:
        """
        return self.task_assigned == 'call' and self.call < self.max_simultaneous_calls and self.is_free and not self.wants_break

    def answer_chat(self, client):
        """
        Agent answers chat
        Allow up to 3
        @param client:
        @return:
        """
        self.chats += 1
        if self.chats == self.max_simultaneous_chats:
            self.is_free = False
        chat_time = Probabilities.chat_duration(client)
        return chat_time

    def answer_call(self, client):
        """
        Agent answers call (currently allows 1 simultaneous calls, but that can be changed)
        @param client:
        @return:
        """
        self.call += 1
        if self.call == self.max_simultaneous_calls:
            self.is_free = False
        call_time = Probabilities.call_duration(client)
        return call_time

    def end_call_or_chat(self):
        """
        End a call or a chat for an agent, decide to go on a break
        @return:
        """
        if self.task_assigned == 'call':
            self.call -= 1
        else:
            self.chats -= 1
        wants_short_break = Probabilities.agent_short_break()
        wants_long_break = Probabilities.agent_long_break()
        if wants_short_break:
            if self.call == 0 and self.chats == 0 and self.n_short_breaks < self.max_short_breaks:
                self.n_short_breaks += 1
                self.on_break = True
                self.wants_break = False
                break_time = 2.0 * 60  # Randomize this
                return break_time  # return break time

        elif wants_long_break:
            if self.call == 0 and self.chats == 0 and self.n_long_breaks < self.max_long_breaks:
                self.n_long_breaks += 1
                self.on_break = True
                self.wants_break = False
                break_time = 5.0 * 60  # Randomize this
                return break_time  # return break time
        else:
            return 0  # No break

        # set terms for breaks
        # Probability to take a break
        # Push to heap being free
