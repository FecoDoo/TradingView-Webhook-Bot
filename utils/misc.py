from time import time


def get_timestamp():
    timestamp = time.strftime("%Y-%m-%d %X")
    return timestamp
