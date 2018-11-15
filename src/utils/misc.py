import time


def time_it(func):
    """
    Decorator to time the function
    """

    def wrapper(*args, **kwargs):
        start = time.time()

        r = func(*args, **kwargs)

        end = time.time()

        delta_sec = end - start
        min, sec = divmod(delta_sec, 60)
        hour, min = divmod(min, 60)
        time_string = (f"\nTime elapsed: Sec: {sec} Min: {min} Hours: {hour}")
        print(time_string)
        return r

    return wrapper
