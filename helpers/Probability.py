# Distribution of clients from sectors - High tech, government, blue-collar
# Distribution of weather - rainy, really hot
# Holidays
# Special Events
# CustomerAgent break hours
# Distribution of call time - if client is over 50 or blue collar assume call takes longer
import datetime


class Probabilities:
    """
    Given specific parameters, return a probability for an event to occur
    """
    def __init__(self, time_of_day, date: datetime.datetime, is_holiday=False):
        self.time_of_day = time_of_day
        self.date = date
        self.is_holiday = is_holiday

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
                   'high-tech':()}

        if client.sector == '':
            pass

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
    my_date = datetime.datetime(2019, 12, 12)
    ps = Probabilities("16", my_date)
    print(ps.weather_probabilities())

