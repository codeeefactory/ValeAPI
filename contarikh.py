from datetime import datetime
import pytz
from convertdate import persian
def convert_to_jalali(date):
    # Given UTC datetime string
    # utc_time_str = '2025-03-30T18:40:01+00:00'

    # Parse the datetime string to a timezone-aware datetime object
    utc_time = datetime.fromisoformat(date)

    # Define Tehran time zone
    tehran_tz = pytz.timezone('Asia/Tehran')

    # Convert the UTC datetime object to Tehran time
    tehran_time = utc_time.astimezone(tehran_tz)

    # Get the Persian date from the Tehran time (use convertdate.persian)
    persian_date = persian.from_gregorian(tehran_time.year, tehran_time.month, tehran_time.day)
    tehran_time_str = tehran_time.strftime("%Y-%m-%d %H:%M:%S")

    persian_date_str = f"{persian_date[0]}/{persian_date[1]}/{persian_date[2]}"
    return persian_date_str


    # # Print Tehran datetime and Persian date
    # print("Tehran Datetime:", tehran_time)
    # print("Persian Date:", persian_date)



def convert_to_thr(date):
    # Given UTC datetime string
    # utc_time_str = '2025-03-30T18:40:01+00:00'

    # Parse the datetime string to a timezone-aware datetime object
    utc_time = datetime.fromisoformat(date)

    # Define Tehran time zone
    tehran_tz = pytz.timezone('Asia/Tehran')

    # Convert the UTC datetime object to Tehran time
    tehran_time = utc_time.astimezone(tehran_tz)

    # Get the Persian date from the Tehran time (use convertdate.persian)
    persian_date = persian.from_gregorian(tehran_time.year, tehran_time.month, tehran_time.day)
    tehran_time_str = tehran_time.strftime("%Y-%m-%d %H:%M:%S")

    # persian_date_str = f"{persian_date[0]}/{persian_date[1]}/{persian_date[2]}"
    return tehran_time_str