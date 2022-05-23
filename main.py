from dataclasses import dataclass
from haversine import haversine

from clean_records import clean_data
from utils import get_moving_rate_to_apply


def calculate_rates():
    with open("./filtered.csv", "r") as f:
        lines = f.readlines()
        routes = {}
        total = 0
        idle_hours = 0
        for index, _ in enumerate(lines):
            if index + 1 < len(lines):
                line1 = lines[index].strip().split(",")
                line2 = lines[index + 1].strip().split(",")
                ride_id = line1[0]

                # check if lines belong to the same route
                if not line1[0] == line2[0]:
                    routes[ride_id] = total + idle_hours * 11.9
                    print(total + idle_hours * 11.9)
                    total = 0
                    idle_hours = 0
                    continue

                coordinate1 = (float(line1[1]), float(line1[2]))
                coordinate2 = (float(line2[1]), float(line2[2]))
                elapsed_seconds = int(line2[3]) - int(line1[3])
                distance_km = haversine(coordinate1, coordinate2)
                km_per_hour = distance_km / (elapsed_seconds / 3600)

                if km_per_hour > 10:
                    total += distance_km * get_moving_rate_to_apply(int(line2[3]))
                else:
                    idle_hours += elapsed_seconds / 3600

            else:
                routes[ride_id] = total + idle_hours * 11.9
                print(total + idle_hours * 11.9)
                total = 0
                idle_hours = 0
                # print(routes[ride_id])
                # if ride_id != '1':
                #    break
        # print(ride_id)
        print(routes)
        with open("./rates.csv", "w") as f:
            # print(routes.keys())
            for id in routes.keys():
                f.write(",".join([id, str(routes[id])]) + "\n")


def main():
    clean_data()
    calculate_rates()


# executes main function
if __name__ == "__main__":
    main()
