from datetime import datetime, timedelta
from typing import Union

def check_date(date_string: str) -> bool:
    """
    Checks if a date string is in the format 'YYYY-MM-DD'.
    
    Parameters
    ----------
    date_string : str
        date in string format

    Returns
    -------
    Bool
        True is in the format 'YYYY-MM-DD' else false.
    """
    try:
        date = datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except Exception as e:
        return False

def safe_convert_date(date_string: Union[str, datetime]) -> datetime:
    """
    Converts a date string to a datetime object if it is in the format 'YYYY-MM-DD'.
    
    Parameters
    ----------
    date_string : str | datetime
        date in string format

    Returns
    -------
    datetime
        datetime object of the date string
    """
    if isinstance(date_string, datetime):
        return date_string
    elif isinstance(date_string, str):
        if check_date(date_string):
            return datetime.strptime(date_string, '%Y-%m-%d')
        else:
            raise ValueError("date_string must be in the format 'YYYY-MM-DD'")
    else:
        raise ValueError("date_string must be a string or datetime object")
