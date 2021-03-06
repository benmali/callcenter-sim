# Distribution of clients from sectors - High tech, government, blue-collar
# Distribution of weather - rainy, really hot
# Holidays
# Special Events
# CustomerAgent break hours
# Distribution of call time - if client is over 50 or blue collar assume call takes longer

import datetime
import numpy as np
import randomname


class Probabilities:
    """
    Given specific parameters, return a probability for an event to occur
    """
    client_patience_ex = None
    client_patience_var = None
    rain_factor = 1.3
    proportion_of_calls_high_tech = 0.02
    proportion_of_calls_industry = 0.05
    holiday = None

    def __init__(self, time_of_day, date: datetime.datetime):
        self.time_of_day = time_of_day
        self.date = date

    @staticmethod
    def max_client_patience() -> datetime.timedelta:
        """
        Generate amount of time, if the client has to wait more than that time, abandon the queue
        Assuming client type and client sector are not correlated
        @return: max_wait_time:maximum wait time a client is willing to wait for a service before abandoning the queue
        """
        expected = Probabilities.client_patience_ex
        variance = Probabilities.client_patience_var
        max_wait_time = datetime.timedelta(minutes=np.random.normal(expected, variance))
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


    @staticmethod
    def contact_rate(curr_hour: datetime.datetime, rest_queue_len: int, n_high_tech:int, n_industry:int, weather=None):
        """
        Return the time between calls depending on the hour of the day
        Formula is x ~ Pois(100) (100 clients/ 1 hour) -> x ~ Exp(1 / 100) (time between clients, in hours)
        We assume the more restaurants in the queue, generates 2% per restaurant
        Therefore we multiply the arrival rate by 1.02 * times the restaurants in queue
        @param weather: rainy or sunny
        @param curr_hour: datetime of current hour
        @return: return time between arrivals (hours)
        """

        holiday_factor = 1.1
        if weather == 'rainy':
            weather_factor = Probabilities.rain_factor
        else:
            weather_factor = 1

        if Probabilities.holiday == 'Yes':
            # we set the factor as the max between holiday or rain
            if weather == 'rainy':
                weather_factor = max(holiday_factor, weather_factor)
            else:
                weather_factor = holiday_factor

        high_tech_prop = Probabilities.proportion_of_calls_high_tech
        industry_prop = Probabilities.proportion_of_calls_industry
        hour_factors = [320, 42.6, 18.28, 14.5, 12.3, 9.19, 8.64, 16, 24.61, 35.5, 45.71, 53.3, 71.1, 91.42, 160, 250]
        h_factor_map = {hour: hour_factors[i] for i, hour in enumerate(range(8, 24))}
        base_rate = (n_high_tech * high_tech_prop + n_industry * industry_prop) / h_factor_map[curr_hour.hour]
        return np.random.exponential(1 / (base_rate * weather_factor * 1.02 ** rest_queue_len))

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

            #return np.random.uniform(2, 5) * 60  # Greater variance for blue collar
            return np.random.normal(3.5 * 60, 60)
        else:
            return np.random.normal(2.5 * 60, 60)
            #return np.random.uniform(2, 3) * 60

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
            return np.random.normal(12 * 60, 240)
            #return np.random.uniform(8, 20) * 60
        else:
            return np.random.normal(9 * 60, 240)
            #return np.random.uniform(5, 15) * 60

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

