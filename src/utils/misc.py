import time
import datetime


def hms(t):
    min, sec = divmod(t, 60)
    hour, min = divmod(min, 60)

    return hour, min, sec


def time_it(func):
    """
    Decorator to time the function
    """

    def wrapper(*args, **kwargs):
        print(f'\n Starting at {datetime.datetime.now()}\n')

        start = time.time()

        r = func(*args, **kwargs)

        end = time.time()

        delta_sec = end - start
        hour, min, sec = hms(delta_sec)
        time_string = (f"\nTime elapsed: Sec: {sec} Min: {min} Hours: {hour}")
        print(time_string)
        return r

    return wrapper
