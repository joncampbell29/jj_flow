from datetime import datetime, timedelta


def check_date(date_string):
    try:
        date = datetime.strptime(date_string, '%Y-%m-%d')
        diff = datetime.now() - date
        return True
    except Exception as e:
        return False