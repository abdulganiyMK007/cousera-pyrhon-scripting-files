"""
Coursera Python Programming Essentials Project Week 4
"""

import datetime


def days_in_month(year, month):
    '''
    Inputs:
    year  - an integer between datetime.MINYEAR and datetime.MAXYEAR
            representing the year
    month - an integer between 1 and 12 representing the month

    Returns:
    The number of days in the input month.
    '''
    date1 = datetime.date(year, month, 1)

    if month == 12:
        month = 1
        year += 1
    else:
        month += 1

    date2 = datetime.date(year, month, 1)
    diff = date2 - date1
    return diff.days


def is_valid_date(year, month, day):
    '''
    Inputs:
    year  - an integer representing the year
    month - an integer representing the month
    day   - an integer representing the day

    Returns:
    True if year-month-day is a valid date and
    False otherwise
    '''
    is_valid_year = (datetime.MINYEAR <= year <= datetime.MAXYEAR)
    if is_valid_year is False:
        return False

    is_valid_month = (1 <= month <= 12)
    if is_valid_month is False:
        return False
    
    is_valid_day = (1 <= day <= days_in_month(year, month))
    if is_valid_day is False:
        return False
    else:
        return True


def days_between(year1, month1, day1, year2, month2, day2):
    '''
    Inputs:
    year1  - an integer representing the year of the first date
    month1 - an integer representing the month of the first date
    day1   - an integer representing the day of the first date
    year2  - an integer representing the year of the second date
    month2 - an integer representing the month of the second date
    day2   - an integer representing the day of the second date

    Returns:
    The number of days from the first date to the second date.
    Returns 0 if either date is invalid or the second date is before the first date.
    '''
    date1_is_valid = is_valid_date(year1, month1, day1)
    date2_is_valid = is_valid_date(year2, month2, day2)

    if (date1_is_valid and date2_is_valid):
        date1 = datetime.date(year1, month1, day1)
        date2 = datetime.date(year2, month2, day2)
        diff = date2 - date1

        if diff.days > 0:
            return diff.days
        else:
            return 0
    else:
        return 0


def age_in_days(year, month, day):
    '''
    Inputs:
    year  - an integer representing the birthday year
    month - an integer representing the birthday month
    day   - an integer representing the birthday day

    Returns:
    The age of a person with the input birthday as of today.
    Returns 0 if the input date is invalid of if the input
    date is in the future.
    '''
    today = datetime.date.today()
    return days_between(year, month, day, today.year, today.month, today.day)



