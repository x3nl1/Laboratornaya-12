from unittest.mock import MagicMock

from app.routers.analytics import ride_stats
from app.routers.drivers import create_driver, get_drivers
from app.main import root
from app.schemas import DriverCreate


def test_ride_stats_with_data():
    db = MagicMock()

    rides = [
        MagicMock(price=100.0),
        MagicMock(price=250.5)
    ]

    db.query.return_value.all.return_value = rides

    result = ride_stats(db)

    assert result['total_rides'] == 2
    assert result['total_revenue'] == 350.5


def test_ride_stats_empty_list():
    db = MagicMock()
    db.query.return_value.all.return_value = []

    result = ride_stats(db)

    assert result['total_rides'] == 0
    assert result['total_revenue'] == 0


def test_create_driver_success():
    db = MagicMock()

    driver = DriverCreate(
        name='John',
        car_model='Toyota',
        plate_number='ABC123'
    )

    result = create_driver(driver, db)

    assert result.name == 'John'
    db.add.assert_called_once()
    db.commit.assert_called_once()


def test_get_drivers():
    db = MagicMock()
    drivers = [MagicMock(name='John')]

    db.query.return_value.all.return_value = drivers

    result = get_drivers(db)

    assert len(result) == 1


def test_root_endpoint():
    result = root()

    assert result['message'] == 'Taxi Service API'
