from pydantic import ValidationError
from domain.models import RideRecord
from utils import (
    is_valid_segment,
    records_belongs_same_route,
    records_has_same_timestamp,
)


def perform_clean_data(rows) -> dict:
    # initial values
    routes = {}
    idx_record1 = 0
    idx_record2 = 1
    is_first_record = True

    while idx_record2 < len(rows):

        try:
            record1 = RideRecord(*rows[idx_record1].strip().split(","))
        except ValidationError:
            idx_record1 += 1
            idx_record2 += 1
            continue

        try:
            record2 = RideRecord(*rows[idx_record2].strip().split(","))
        except ValidationError:
            idx_record2 += 1
            continue

        if not records_belongs_same_route(record1, record2):
            idx_record1 = idx_record2
            idx_record2 = idx_record1 + 1
            is_first_record = True
            continue

        ride_id = record1.ride_id

        # creating ride key in dictionary
        if not routes.get(ride_id):
            routes[ride_id] = []

        if is_first_record:
            routes[ride_id].append(record1)

        if records_has_same_timestamp(record1, record2):
            idx_record2 += 1
            continue

        if is_valid_segment(record1, record2):
            routes[ride_id].append(record2)
            idx_record1 = idx_record2

        idx_record2 += 1
        is_first_record = False

    return routes


def clean_data():
    with open("./paths.csv", "r") as f:
        lines = f.readlines()
        routes = perform_clean_data(lines)
        with open("./filtered.csv", "w") as f:
            for id in routes.keys():
                for line in routes[id]:
                    f.write(str(line) + "\n")
