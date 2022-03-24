import datetime


class TimeHelper:

    @classmethod
    def get_month_number(cls, time: datetime.datetime) -> str:
        """
        Given a date time object, return number of the month
        @param time: datetime object
        @return:
        """
        return time.strftime("%m")
