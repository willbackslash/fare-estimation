import os
import pytz
import datetime
from haversine import haversine


def records_belongs_same_route(record1, record2):
    return record1.ride_id == record2.ride_id


def records_has_same_timestamp(record1, record2):
    return int(record2.timestamp) - int(record1.timestamp) == 0


def timestamp_to_datetime(timestamp: int):
    tz = pytz.timezone(os.getenv("TIMEZONE", "UTC"))
    return datetime.datetime.fromtimestamp(timestamp, tz)


def is_valid_segment(record1, record2) -> bool:
    coordinate1 = (float(record1.latitude), float(record1.longitude))
    coordinate2 = (float(record2.latitude), float(record2.longitude))
    elapsed_seconds = int(record2.timestamp) - int(record1.timestamp)
    distance_km = haversine(coordinate1, coordinate2)
    km_per_hour = distance_km / (elapsed_seconds / 3600)

    return not km_per_hour > 100


def get_moving_rate_to_apply(timestamp: int):
    timestamp_datetime = timestamp_to_datetime(timestamp)
    time = timestamp_datetime.time()

    if time > datetime.time(0, 0, 0) and time <= datetime.time(5, 0, 0):
        return 1.30

    return 0.74
