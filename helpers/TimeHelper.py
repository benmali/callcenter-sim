import datetime


class TimeHelper:

    @staticmethod
    def get_month_number(time: datetime.datetime) -> str:
        """
        Given a date time object, return number of the month
        @param time: datetime object
        @return:
        """
        return time.strftime("%m")

    @staticmethod
    def add_days(current_date: datetime.datetime, n_days_to_add: int) -> datetime.datetime:
        """
        Get the date of a given date + number of days ahead
        @param current_date: the base date to calculate from
        @param n_days_to_add: number of days to add
        @return: datetime.datetime (date)
        """
        return current_date + datetime.timedelta(days=n_days_to_add)

    @staticmethod
    def string_to_date(date: str) -> datetime.datetime:
        """
        Convert a date string to date time
        @param date:
        @return:
        """
        return datetime.datetime.strptime(date, '%d-%m-%Y')

    @staticmethod
    def string_to_hour(hour: str) -> datetime.datetime:
        """
        Convert string to datetime object
        @param hour:
        @return:
        """
        return datetime.datetime.strptime(hour, '%H:%M:%S')

    @staticmethod
    def string__to_full_time(date: str) -> datetime:
        return datetime.datetime.strptime(date, '%d-%m-%Y %H:%M:%S')

    @staticmethod
    def set_next_day(date: datetime.datetime) -> datetime.datetime:
        month = date.month
        day = date.day
        year = date.year

        return datetime.datetime.strptime(f'{day}-{month}-{year} 08:00:00', '%d-%m-%Y %H:%M:%S') + \
               datetime.timedelta(days=1)
