from pydantic.dataclasses import dataclass


@dataclass
class RideRecord:
    ride_id: str
    latitude: float
    longitude: float
    timestamp: int

    def __str__(self) -> str:
        return f"{self.ride_id},{self.latitude},{self.longitude},{self.timestamp}"
