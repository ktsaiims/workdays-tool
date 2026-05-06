import numpy as np
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

def count_workdays(start_date: np.datetime64, end_date: np.datetime64) -> int:
    '''Count number of workdays between two dates.

    Args:
        start_date: numpy datetime64 object
        end_date: numpy datetime64 object

    Returns:
        Number of workdays (Mon-Fri)
    '''
    return int(np.busday_count(start_date, end_date))
