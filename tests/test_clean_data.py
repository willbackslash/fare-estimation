import pytest
from domain.models import RideRecord
from pydantic import ValidationError


def test_given_a_valid_row_it_instantiates_a_valid_ride_record():
    row = "1,37.966660,23.728308,1405594957"
    record = RideRecord(*row.strip().split(","))
    assert record.ride_id == "1"
    assert record.latitude == 37.966660
    assert record.longitude == 23.728308
    assert record.timestamp == 1405594957


def test_given_an_invalid_row_it_raises_an_exception():
    row = "1,a,23.728308,1405594957"
    with pytest.raises(ValidationError):
        record = RideRecord(*row.strip().split(","))
