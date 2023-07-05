import time


def display_running_time(func):
    def wrapper(*args, **kwargs):

        start_time = time.time()

        result = func(*args, **kwargs)

        took_secs = round(time.time() - start_time, 3)

        print(f" {func.__name__:<50} | Took | {took_secs} seconds ")

        return result

    return wrapper
