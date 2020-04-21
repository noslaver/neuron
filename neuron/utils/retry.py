import time

def retry(func, times, wait=100):
    attempts = 0

    while True:
        try:
            return func()
        except Exception as e:
            attempts += 1
            if attempts == times:
                raise e
            time.sleep((100 * (times + 1)) / 1000)
