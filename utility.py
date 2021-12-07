from datetime import date, datetime, time, tzinfo
from dateutil import parser, tz

def convert_soql_date_to_datetime(dt_str: str):
    return parser.parse(dt_str)

def convert_date_to_soql(dt, convert_to_datetime: bool=False, use_utc_time: bool=True):
    soql_time = ''
    date_part = '1980-01-26'
    time_part = '00:00:01.000'
    # tz_nyc = tz.gettz('Eastern Standard Time')
    # tz_utc = tz.gettz('UTC')
    tz_nyc = '-05:00'
    tz_utc = 'Z'

    tz_str = tz_utc if use_utc_time else tz_nyc

    if isinstance(dt, datetime):
        return dt.isoformat() + tz_str
    elif isinstance(dt, date):
        return dt.isoformat() + 'T' + time_part + tz_str
    elif isinstance(dt, str):
        dt = parser.parse(dt)
        return dt.isoformat() # dateutil assumes UTC for tzinfo if no offset is found
    else:
        return None