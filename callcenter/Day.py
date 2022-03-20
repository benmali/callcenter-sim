class Day:
    def __init__(self, day_date, is_rainy, is_hot, is_cold):
        """
        Class to represent a day
        :param day_date: The date of the day instance
        :param is_rainy: T/F is the day rainy
        """
        self.is_rainy = is_rainy
        self.is_hot = is_hot
        self.is_cold = is_cold
        self.day_date = day_date
        self.day_name = self._set_day_name()

    def __repr__(self):
        return f""

    def _set_day_name(self) -> str:
        """
        Calculate the day of the week from the date
        :return:
        """
        x = self.day_date
        return ""


