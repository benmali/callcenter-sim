# Distribution of clients from sectors - High tech, government, blue-collar
# Distribution of weather - rainy, really hot
# Holidays
# Special Events
# CustomerAgent break hours
# Distribution of call time - if client is over 50 or blue collar assume call takes longer

# What is the company signing rate (how often we have a signing?- distribution?)
# We assume a company signing is unrelated to other companies signing
import datetime
import numpy as np
import randomname


class Probabilities:
    """
    Given specific parameters, return a probability for an event to occur
    """

    def __init__(self, time_of_day, date: datetime.datetime, is_holiday=False):
        self.time_of_day = time_of_day
        self.date = date
        self.is_holiday = is_holiday

    @staticmethod
    def company_sign_rate() -> int:
        """
        Set the rate of company signing (once a month, twice a month.. etc)
        The number of days to next company sign
        (This should be some poisson distribution)
        @return:
        """
        return np.random.randint(60, 120)

    @staticmethod
    def restaurant_sign_rate() -> int:
        """
        Set the rate of which restaurants are added to the service
        (This should be some poisson distribution)
        @return:
        """
        return np.random.randint(60, 120)

    @staticmethod
    def create_random_rest_name():
        name = randomname.get_name()
        return name

    @staticmethod
    def company_size_and_sector_distribution():
        """
        Company size is correlated with company sector
        Chance to be high tech company is 70%
        Given the number, randomize a sector
        Chance to be small, medium, big, corporate = 0.6 (x <50 ), 0.25 ( 50< x < 500) 0.10 ( 500< x< 1000) 0.04 (x>1000)
        0.01 government
        You can change this probability to reflect the real chance for  a company signing
        We assume a company signing is unrelated to other companies signing
        @return:
        """

        probability = np.random.uniform()
        if probability <= 0.5:
            n_employees = np.random.uniform(10, 50)  # Number of employees for a small company
        elif 0.5 < probability < 0.85:
            n_employees = np.random.uniform(50, 500)
        elif 0.85 < probability < 0.95:
            n_employees = np.random.uniform(500, 1000)

        elif 0.95 < probability < 0.99:
            n_employees = np.random.uniform(1000, 1500)
        else:
            n_employees = np.random.uniform(1500, 50000)  # Government, few global companies

        probability = np.random.uniform()  # Define a dependent probability for sector
        if 10 <= n_employees <= 50:
            if probability < 0.2:
                sector = "Blue-Collar"
            else:
                sector = "High-Tech"
        elif 50 < n_employees <= 500:
            if probability < 0.5:
                sector = "Blue-Collar"
            else:
                sector = "High-Tech"
        elif 500 < n_employees <= 1000:
            if probability < 0.3:
                sector = "Blue-Collar"
            else:
                sector = "High-Tech"
        elif 1000 < n_employees <= 1500:
            if probability < 0.15:
                sector = "Blue-Collar"
            else:
                sector = "High-Tech"
        else:
            if probability < 0.9:  # Not many high tech companies that size, most likely government companies
                sector = "Blue-Collar"
            else:
                sector = "High-Tech"
        return n_employees, sector

    def contact_probabilities(self, client):
        """
        If we decided that the client will contact the call center, decide how
        Tuple represents probabilities
        @param client:
        @return:
        """
        # parameters on contact channel are sectors and age - weather decided if the call center will be contacted at all
        # Given we have a rainy day -> more calls for orders -> more where is my food (otherwise people just walk)
        # Given a sector and age -> reset my password/login issues
        sectors = {'blue-collar': (0.75, 0.25),
                   'high-tech': ()}

        if client.sector == '':
            pass

    @staticmethod
    def call_rate(curr_hour: datetime.datetime):
        """
        Return the time between calls depending on the hour of the day
        @param curr_hour:
        @return:
        """
        if curr_hour.hour < 11:
            return np.random.exponential(1 / 100)
        elif 11 <= curr_hour.hour <= 14:
            return np.random.exponential(1/60)
        else:
            return np.random.exponential(1 / 120)

    @staticmethod
    def chat_rate(curr_hour: datetime.datetime):
        """
        Return the time between chats depending on the hour of the day
        @param curr_hour:
        @return:
        """
        if curr_hour.hour < 11:
            return np.random.exponential(1 / 100)
        elif 11 <= curr_hour.hour <= 14:
            return np.random.exponential(1/60)
        else:
            return np.random.exponential(1 / 120)

    @staticmethod
    def call_duration(client) -> float:
        """
        Depending on the client, randomize a call duration
        Assume call duration for blue collar will be longer
        @param client:
        @return:
        """
        if client.sector == 'Blue-Collar':
            return 5.13
        else:
            return 3.0

    @staticmethod
    def chat_duration(client) -> float:
        """
        Depending on the client, randomize a call duration
        Assume call duration for blue collar will be longer
        @param client:
        @return:
        """
        if client.sector == 'Blue-Collar':
            return 5.13
        else:
            return 3.0

    def weather_probabilities(self):
        """
        We assess these probabilities from statistics we gather
        You can replace this with real ones, with a more fined grained resolution (probability per day for example)
        """
        months_rain_probabilities = {
            "01": 0.35,
            "02": 0.20,
            "03": 0.10,
            "04": 0.02,
            "05": 0.001,
            "06": 0.001,
            "07": 0.001,
            "08": 0.0001,
            "09": 0.05,
            "10": 0.15,
            "11": 0.25,
            "12": 0.35
        }
        return months_rain_probabilities[self.date.strftime("%m")]


if __name__ == "__main__":
    # my_date = datetime.datetime(2019, 12, 12)
    # ps = Probabilities("16", my_date)
    # print(ps.weather_probabilities())
    print(Probabilities.create_random_rest_name())
