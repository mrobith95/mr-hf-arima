from datetime import datetime

def str2datetime(s: str) -> datetime:
    """
    Convert a string with format YYYY-MM-DD hh:mm:ss.us+tz to a datetime object.
    If the timezone offset is in the format '+HH:MM', this function removes the colon.
    """
    # Check if timezone offset has a colon (e.g., +08:00)
    if len(s) >= 6 and s[-3] == ":":
        # Remove the colon in the timezone part, e.g. convert '+08:00' to '+0800'
        s = s[:-3] + s[-2:]
    return datetime.strptime(s, "%Y-%m-%d %H:%M:%S.%f%z")