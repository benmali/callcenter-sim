from helpers.Probability import Probabilities


class Restaurant:
    def __init__(self,  location):
        self.name = Probabilities.create_random_rest_name()
        self.location = location
        self.calls = []

    def __repr__(self):
        return self.name

    def ran_out_of_ingredient(self):
        """
        Use this method to generate a CALL if ran out of something in the middle of day
        @return:
        """
        pass

    def can_supply_order(self):
        """
        If something ran out, clients are still ordering this and we cant supply it
        App still shows it's available
        @return:
        """
        pass