import datetime as dt

from loguru import logger

TEST_TIMES = [dt.datetime(2023,8,11,10,25,0), dt.datetime(2023,8,11,16,14,0), dt.datetime(2023,8,11,23,59,0), dt.datetime(2023,8,11,6,8,0)]



@logger.catch
def stamp_ready_time(express=False, time_create=dt.datetime.now()):

    if time_create.hour >= 13 and time_create.hour <= 17:
        ready_time = time_create + dt.timedelta(days=1)
        ready_time = ready_time.replace(hour=10, minute=00, second=0)
    elif time_create.hour >= 0 and time_create.hour <= 12:
        ready_time = time_create
        ready_time = ready_time.replace(hour=15, minute=00, second=0)
    else:
        ready_time = time_create + dt.timedelta(days=1)
        ready_time = ready_time.replace(hour=15, minute=00, second=0)

    if express:
        if time_create.hour >= 10 and time_create.hour <= 17:
            ready_time = time_create + dt.timedelta(hours=1)
        elif time_create.hour >= 0 and time_create.hour <= 10:
            ready_time = time_create.replace(hour=11, minute=00, second=0)
        else:
            ready_time = time_create + dt.timedelta(days=1)
            ready_time = ready_time.replace(hour=10, minute=00, second=0)
    
    if ready_time.weekday() >= 5:
        while ready_time.weekday() != 0:
            ready_time += dt.timedelta(days=1)

    return ready_time


if __name__ == '__main__':
    pass