from datetime import datetime, timedelta

#####
# Need function to check that a date string is in the format YYYY-MM-DD. Returns true if the date is in the right format, false otherwise
# Need function to convert date strings to datetime objects
# Need function to produce a date range given time before (i.e. 1 year ago, 10 days ago, 5 years ago, etc) and end date 
####
def check_date(date_string):
    try:
        date = datetime.strptime(date_string, '%Y-%m-%d')
        diff = datetime.now() - date
        return True
    except Exception as e:
        return False