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
        return datetime.datetime.strptime(date, '%d-%m-%y')


    @staticmethod
    def get_date_isr_format(date: datetime.datetime) -> str:
        """
        Get the desired date in Israeli time format
        @param date:
        @return:
        """
        pass
