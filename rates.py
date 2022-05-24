from haversine import haversine
from domain.models import RideRecord
from utils import (
    get_distance,
    get_elapsed_time,
    get_moving_rate_to_apply,
    get_segment_velocity,
    records_belongs_same_route,
)


def get_final_rate(total_moving_rate, total_idle_hours):
    flag_rate = 1.30
    final_rate = flag_rate + total_moving_rate + total_idle_hours * 11.9

    if final_rate < 3.47:
        final_rate = 3.47

    return round(final_rate, 2)


def perform_rates_calculation(records):
    # initial values
    rates = {}
    idx_record1 = 0
    idx_record2 = 1
    total = 0
    idle_hours = 0

    while idx_record2 < len(records):
        record1 = RideRecord(*records[idx_record1].strip().split(","))
        record2 = RideRecord(*records[idx_record2].strip().split(","))
        ride_id = record1.ride_id

        if not records_belongs_same_route(record1, record2):
            # stores the total rate for the previous route
            rates[ride_id] = get_final_rate(total, idle_hours)

            # restarts initial data for next route
            total = 0
            idle_hours = 0
            idx_record1 += 1
            idx_record2 += 1
            continue

        distance_km = get_distance(record1, record2)
        km_per_hour = get_segment_velocity(record1, record2)
        elapsed_seconds = get_elapsed_time(record1, record2)

        if km_per_hour > 10:
            total += distance_km * get_moving_rate_to_apply(record2.timestamp)
        else:
            idle_hours += elapsed_seconds / 3600

        idx_record1 += 1
        idx_record2 += 1

    # gets the final rate for the last ride
    rates[ride_id] = get_final_rate(total, idle_hours)

    return rates


def calculate_rates():
    with open("./filtered.csv", "r") as f:
        records = f.readlines()
        rates = perform_rates_calculation(records)
        with open("./rates.csv", "w") as f:
            for id in rates.keys():
                print(id, "{:.2f}".format(rates[id]))
                f.write(",".join([id, "{:.2f}".format(rates[id])]) + "\n")
