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
    def max_client_patience() -> datetime.timedelta:
        """
        Generate amount of time, if the client has to wait more than that time, abandon the queue
        Assuming client type and client sector are not correlated
        @return: max_wait_time:maximum wait time a client is willing to wait for a service before abandoning the queue
        """
        max_wait_time = datetime.timedelta(minutes=np.random.normal(10.0, 1.5))
        return max_wait_time

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
    def contact_rate(curr_hour: datetime.datetime, rest_queue_len: int, weather=None):
        """
        Return the time between calls depending on the hour of the day
        Formula is x ~ Pois(100) (100 clients/ 1 hour) -> x ~ Exp(1 / 100) (time between clients, in hours)
        We assume the more restaurants in the queue, generates 2% per restaurant
        Therefore we multiply the arrival rate by 1.02 * times the restaurants in queue
        @param curr_hour:
        @return:
        """
        if weather == 'rainy':
            weather_factor = 1.3
        else:
            weather_factor = 1

        if curr_hour.hour == 8:
            return np.random.exponential(1 / (10 * weather_factor * 1.02 ** rest_queue_len))
        elif curr_hour.hour == 9:
            return np.random.exponential(1 / (75 * weather_factor * 1.02 ** rest_queue_len))
        elif curr_hour.hour == 10:
            return np.random.exponential(1 / (175 * weather_factor * 1.02 ** rest_queue_len))
        elif curr_hour.hour == 11:
            return np.random.exponential(1 / (250 * weather_factor * 1.02 ** rest_queue_len))
        elif curr_hour.hour == 12:
            return np.random.exponential(1 / (300 * weather_factor * 1.02 ** rest_queue_len))
        elif curr_hour.hour == 13:
            return np.random.exponential(1 / (400 * weather_factor * 1.02 ** rest_queue_len))
        elif curr_hour.hour == 14:
            return np.random.exponential(1 / (430 * weather_factor * 1.02 ** rest_queue_len))
        elif curr_hour.hour == 15:
            return np.random.exponential(1 / (200 * weather_factor * 1.02 ** rest_queue_len))
        elif curr_hour.hour == 16:
            return np.random.exponential(1 / (130 * weather_factor * 1.02 ** rest_queue_len))
        elif curr_hour.hour == 17:
            return np.random.exponential(1 / (90 * weather_factor * 1.02 ** rest_queue_len))
        elif curr_hour.hour == 18:
            return np.random.exponential(1 / (75 * weather_factor * 1.02 ** rest_queue_len))
        elif curr_hour.hour == 19:
            return np.random.exponential(1 / (60 * weather_factor * 1.02 ** rest_queue_len))
        elif curr_hour.hour == 20:
            return np.random.exponential(1 / (45 * weather_factor * 1.02 ** rest_queue_len))
        elif curr_hour.hour == 21:
            return np.random.exponential(1 / (35 * weather_factor * 1.02 ** rest_queue_len))
        elif curr_hour.hour == 22:
            return np.random.exponential(1 / (20 * weather_factor * 1.02 ** rest_queue_len))

        else:
            n_arrivals = 120

            return np.random.exponential(1 / 35)

    @staticmethod
    def call_duration(client) -> float:
        """
        Depending on the client, randomize a call duration
        Assume call duration for blue collar will be longer
        Can add contact reason here
        @param client:
        @return:
        """
        if client.sector == 'Restaurant':
            return np.random.uniform(1, 2) * 60

        elif client.sector == 'Blue-Collar':

            return np.random.uniform(2, 5) * 60  # Greater variance for blue collar
        else:
            return np.random.uniform(2, 3) * 60

    @staticmethod
    def contact_duration(client):
        """
        Return the duration of the call or chat with the call center
        @param client: Client or Restaurant
        @return:
        """
        if client.contact_method == "call":
            return Probabilities.call_duration(client)
        else:
            return Probabilities.chat_duration(client)

    @staticmethod
    def chat_duration(client) -> float:
        """
        Depending on the client, randomize a call duration
        Assume call duration for blue collar will be longer
        Can add contact reason here
        @param client:
        @return:
        """
        if client.sector == 'Blue-Collar':
            return np.random.uniform(8, 20) * 60
        else:
            return np.random.uniform(5, 15) * 60

    @staticmethod
    def agent_short_break():
        """
        Randomize if an agent wants a short break
        @return:
        """
        probability = np.random.uniform(0, 1)
        return probability < 0.1

    @staticmethod
    def agent_long_break():
        """
        Randomize if an agent wants a short break
        @return:
        """
        probability = np.random.uniform(0, 1)
        return probability < 0.06

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
    print(1 / np.random.exponential(1 / 2000))  # bigger gap
    print(1 / np.random.exponential(1 / 50))  # smaller gap
