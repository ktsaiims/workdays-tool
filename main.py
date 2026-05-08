import holidays
import numpy as np
import pandas as pd
import streamlit as st
from datetime import datetime


HOLIDAY_EXCLUSIONS = [
    'Birthday of Martin Luther King, Jr.',
    "Washington's Birthday",
    'Veterans Day',
    'Juneteenth National Independence Day',
    'Columbus Day',
    'Christmas Eve',
    'National Day of Mourning'
]

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
    return int(np.busday_count(begindates=start_date, enddates=end_date + 1, holidays=holidays))

def run_calculations(user_year: int) -> tuple[pd.DataFrame, dict[str, int]]:
    start_date = standardize_date(f'{user_year}-01-01')
    end_date = standardize_date(f'{user_year}-12-31')

    us_fed_holidays = holidays.US(years=user_year, categories=holidays.GOVERNMENT)

    # Remove excluded holidays (wildcard match)
    filtered_holidays = {}
    for date, holiday_name in us_fed_holidays.items():
        if not any(word in holiday_name for word in HOLIDAY_EXCLUSIONS):
            day_name = pd.Timestamp(date).day_name()

            if pd.Timestamp(date).dayofweek <= 4: # 0-4 = weekdays; 5-6 = weekends
                filtered_holidays[date] = {
                    'Holiday': holiday_name,
                    'Day': day_name
                }

    # Dataframe of holidays
    df_holidays = pd.DataFrame.from_dict(
        filtered_holidays,
        orient='index'
    )
    df_holidays.index.name = 'Date' # rename index so it shows up as table header
    df_holidays = df_holidays.reset_index()
    df_holidays = df_holidays.sort_values('Date').reset_index(drop=True)

    # List of holiday dates
    holiday_dates = []
    for date in filtered_holidays.keys():
        holiday_dates.append(standardize_date(str(date)))

    # Convert numpy datetime64 to Python datetime
    py_start_date = pd.Timestamp(start_date).to_pydatetime()
    py_end_date = pd.Timestamp(end_date).to_pydatetime()

    cal_workdays = count_workdays(start_date, end_date) # normal calendar workdays
    ims_workdays = count_workdays(start_date, end_date, holiday_dates)
    total_days = (py_end_date - py_start_date).days + 1 # convert timedelta to days for math
    cal_weekends = total_days - cal_workdays

    year_info = {
        'Total Days': total_days,
        'Calendar Workdays': cal_workdays,
        'IMS Workdays': ims_workdays,
        'Weekends': cal_weekends,
        'Holidays': len(filtered_holidays)
    }

    return df_holidays, year_info


if __name__ == '__main__':
    current_year = datetime.now().year
    user_year = st.number_input(f'Enter year (default {current_year}):', value=current_year)

    df_holidays, year_dict = run_calculations(user_year)

    st.title(f'Calendar Year {user_year}', text_alignment='center')

    col1, col2, col3, col4 = st.columns(4)
    col1.metric('Total Days', year_dict['Total Days'])
    col2.metric('Weekends', year_dict['Weekends'])
    col3.metric('IMS Holidays', year_dict['Holidays'])
    col4.metric('IMS Workdays', year_dict['IMS Workdays'])

    st.header('IMS Holidays', text_alignment='center')
    st.text('Holidays that fall on weekends are excluded.')
    st.table(df_holidays)
