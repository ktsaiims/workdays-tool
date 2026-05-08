import holidays
import numpy as np
import streamlit as st
from datetime import datetime


def standardize_date(date: str) -> np.datetime64:
    '''Standardize multiple date formats.

    Args:
        date: Unformatted date

    Returns:
        Date formatted as "yyyy-mm-dd"
    '''
    formats = [
        '%Y-%m-%d', '%Y.%m.%d',
        '%m-%d-%Y', '%m-%d-%y',
        '%m/%d/%Y', '%m/%d/%y',
        '%m.%d.%Y', '%m.%d.%y'
    ]

    for fmt in formats:
        try:
            formatted_date = datetime.strptime(date, fmt).date()
            return np.datetime64(formatted_date)
        except Exception:
            pass

    raise ValueError(f'Unrecognized date (use "yyyy-mm-dd"): {date}')

def is_workday(date: np.datetime64) -> bool:
    '''Check if date is Mon-Fri.

    Args:
        date: numpy datetime64 object

    Returns:
        True or False
    '''
    result = np.is_busday(date)
    if result:
        return True

    return False

def count_workdays(start_date: np.datetime64, end_date: np.datetime64, holidays: list=[]) -> int:
    '''Count number of workdays between two dates.

    Args:
        start_date: numpy datetime64 object
        end_date: numpy datetime64 object

    Returns:
        Number of workdays (Mon-Fri)
    '''
    return int(np.busday_count(begindates=start_date, enddates=end_date, holidays=holidays))


user_year = input('>>Enter year: ')
start_date = standardize_date(f'{user_year}-01-01')
end_date = standardize_date(f'{user_year}-12-31')

HOLIDAY_EXCLUSIONS = [
    'Birthday of Martin Luther King, Jr.',
    "Washington's Birthday",
    'Veterans Day',
    'Juneteenth National Independence Day',
    'Columbus Day',
    'Christmas Eve'
]

us_fed_holidays = holidays.US(years=user_year, categories=holidays.GOVERNMENT)

# Remove excluded holidays (wildcard match)
filtered_holidays = {}
for date, name in us_fed_holidays.items():
    if not any(word in name for word in HOLIDAY_EXCLUSIONS):
        filtered_holidays[date] = name

holiday_dates = []
for date in filtered_holidays.keys():
    holiday_dates.append(standardize_date(str(date)))

num_workdays = count_workdays(start_date, end_date, holiday_dates)



'''
Year: 2026
Workdays: 123

Holidays
#######


'''
