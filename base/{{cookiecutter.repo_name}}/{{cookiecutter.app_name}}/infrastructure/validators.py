from datetime import datetime


def validate_dt(dt: datetime) -> int:
    """Take in a datetime object and validate that is in the future.

    Return the epoch time in seconds.
    """
    # Get the current datetime
    now = datetime.now()

    # Ensure that the request is in the future
    assert dt > now

    # Return the epoch time in seconds
    return dt.timestamp()
