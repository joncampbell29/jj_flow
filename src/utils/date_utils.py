from datetime import datetime, timedelta

def check_date(date_string):
    try:
        date = datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except Exception as e:
        return False

def safe_convert_date(date_string):
    if isinstance(date_string, datetime):
        return date_string
    elif isinstance(date_string, str):
        if check_date(date_string):
            return datetime.strptime(date_string, '%Y-%m-%d')
        else:
            raise ValueError("date_string must be in the format 'YYYY-MM-DD'")
    else:
        raise ValueError("date_string must be a string or datetime object")

# def create_date_range(time_before, end_date):
#     if isinstance(time_before, timedelta):
#         end_date = safe_convert_date(end_date)
#         start_date = end_date - time_before
#         return start_date, end_date
#     else:
#         raise ValueError("time_before must be a `timedelta` object")