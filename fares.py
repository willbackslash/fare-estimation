import datetime
from domain.models import RideRecord
from utils import (
    get_distance,
    get_elapsed_time,
    get_segment_velocity,
    records_belongs_same_route,
    timestamp_to_datetime,
)


def get_final_fare(total_moving_fare, total_idle_hours_fare):
    flag_fare = 1.30
    final_fare = flag_fare + total_moving_fare + total_idle_hours_fare

    if final_fare < 3.47:
        final_fare = 3.47

    return round(final_fare, 2)


def get_segment_total_moving_fare(distance_km, timestamp):
    return distance_km * get_moving_fare_to_apply(timestamp)


def get_segment_idle_hours_fare(record1, record2):
    elapsed_seconds = get_elapsed_time(record1, record2)
    return (elapsed_seconds / 3600) * 11.9


def get_moving_fare_to_apply(timestamp: int):
    timestamp_datetime = timestamp_to_datetime(timestamp)
    time = timestamp_datetime.time()

    if time > datetime.time(0, 0, 0) and time <= datetime.time(5, 0, 0):
        return 1.30

    return 0.74


def perform_fares_calculation(records):
    # initial values
    fares = {}
    idx_record1 = 0
    idx_record2 = 1
    total_moving_fare = 0
    idle_hours_fare = 0

    while idx_record2 < len(records):
        record1 = RideRecord(*records[idx_record1].strip().split(","))
        record2 = RideRecord(*records[idx_record2].strip().split(","))
        ride_id = record1.ride_id

        if not records_belongs_same_route(record1, record2):
            # stores the total fare for the previous route
            fares[ride_id] = get_final_fare(total_moving_fare, idle_hours_fare)

            # restarts initial data for next route
            total_moving_fare = 0
            idle_hours_fare = 0
            idx_record1 += 1
            idx_record2 += 1
            continue

        distance_km = get_distance(record1, record2)
        km_per_hour = get_segment_velocity(record1, record2)

        if km_per_hour > 10:
            total_moving_fare += get_segment_total_moving_fare(
                distance_km, record2.timestamp
            )
        else:
            idle_hours_fare += get_segment_idle_hours_fare(record1, record2)

        idx_record1 += 1
        idx_record2 += 1

    # gets the final fare for the last ride
    fares[ride_id] = get_final_fare(total_moving_fare, idle_hours_fare)

    return fares


def calculate_fares():
    with open("./filtered.csv", "r") as f:
        records = f.readlines()
        fares = perform_fares_calculation(records)
        with open("./fares.csv", "w") as f:
            f.write("id_ride,fare_estimate\n")
            for id in fares.keys():
                print(id, "{:.2f}".format(fares[id]))
                f.write(",".join([id, "{:.2f}".format(fares[id])]) + "\n")
