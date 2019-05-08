"""Various utility functions."""
import datetime
import time
import json
import decimal


def day_diff(timestamp1, timestamp2):
    """Get the difference (in days) between two timestamps.

    Args:
      timestamp1, timestamp2: Int.

    Returns:
      Int.
    """
    date1 = to_date(timestamp1)
    date2 = to_date(timestamp2)
    return (date2 - date1).days


def to_date(timestamp):
    """Convert a timestamp into a DateTime.

    Args:
      timestamp: Integer.

    Returns:
      datetime.datetime.
    """
    if timestamp > 1e11:
        timestamp /= 1e3
    return datetime.datetime.fromtimestamp(timestamp)


def to_str(timestamp):
    d = to_date(timestamp)
    return '%s-%s' % (d.year, d.month)


def to_timestamp(date_time):
    """Get a timestamp from a datetime.

    Args:
      date_time: datetime.datetime.

    Returns:
      Integer.

    Raises:
      ValueError: if not a datetime or a date.
    """
    if isinstance(date_time, datetime.datetime):
        return int(time.mktime(date_time.timetuple()) * 1000
                   + (date_time.microsecond / 1000))
    elif isinstance(date_time, datetime.date):
        return int(time.mktime(date_time.timetuple()) * 1000)
    else:
        raise ValueError('Unexpected type: %r' % type(date_time))


class DecimalEncoder(json.JSONEncoder):
    """For dumping python decimals to JSON.

    Taken from Elias Zamaria's answer here:
    https://stackoverflow.com/questions/1960516/python-json-serialize-a-decimal-object

    Usage:
    json.dumps(decimal.Decimal('10.0'), cls=DecimalEncoder).
    """
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)
