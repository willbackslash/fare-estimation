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


def get_distance(record1, record2):
    coordinate1 = (float(record1.latitude), float(record1.longitude))
    coordinate2 = (float(record2.latitude), float(record2.longitude))

    return haversine(coordinate1, coordinate2)


def get_elapsed_time(record1, record2):
    return int(record2.timestamp) - int(record1.timestamp)


def get_segment_velocity(record1, record2):
    distance_km = get_distance(record1, record2)
    elapsed_seconds = get_elapsed_time(record1, record2)
    km_per_hour = distance_km / (elapsed_seconds / 3600)

    return km_per_hour


def is_valid_segment(record1, record2) -> bool:
    km_per_hour = get_segment_velocity(record1, record2)

    return not km_per_hour > 100
