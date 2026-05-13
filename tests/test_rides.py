import pytest
from fastapi import HTTPException
from unittest.mock import MagicMock

from app.routers.rides import create_ride, get_rides, update_ride, delete_ride
from app.schemas import RideCreate


@pytest.fixture
def ride_data():
    return RideCreate(
        pickup='A',
        destination='B',
        price=100.0,
        user_id=1,
        driver_id=1,
        tariff_id=1
    )


def prepare_db_with_entities():
    db = MagicMock()

    user_query = MagicMock()
    user_query.filter.return_value.first.return_value = object()

    driver_query = MagicMock()
    driver_query.filter.return_value.first.return_value = object()

    tariff_query = MagicMock()
    tariff_query.filter.return_value.first.return_value = object()

    db.query.side_effect = [user_query, driver_query, tariff_query]

    return db


def test_create_ride_success(ride_data):
    db = prepare_db_with_entities()

    result = create_ride(ride_data, db)

    assert result.price == 100.0
    db.add.assert_called_once()
    db.commit.assert_called_once()


def test_create_ride_user_not_found(ride_data):
    db = MagicMock()
    query = MagicMock()
    query.filter.return_value.first.return_value = None
    db.query.return_value = query

    with pytest.raises(HTTPException) as exc:
        create_ride(ride_data, db)

    assert exc.value.status_code == 404
    assert 'User not found' in exc.value.detail


def test_create_ride_driver_not_found(ride_data):
    db = MagicMock()

    user_query = MagicMock()
    user_query.filter.return_value.first.return_value = object()

    driver_query = MagicMock()
    driver_query.filter.return_value.first.return_value = None

    db.query.side_effect = [user_query, driver_query]

    with pytest.raises(HTTPException) as exc:
        create_ride(ride_data, db)

    assert exc.value.status_code == 404


def test_create_ride_tariff_not_found(ride_data):
    db = MagicMock()

    user_query = MagicMock()
    user_query.filter.return_value.first.return_value = object()

    driver_query = MagicMock()
    driver_query.filter.return_value.first.return_value = object()

    tariff_query = MagicMock()
    tariff_query.filter.return_value.first.return_value = None

    db.query.side_effect = [user_query, driver_query, tariff_query]

    with pytest.raises(HTTPException) as exc:
        create_ride(ride_data, db)

    assert exc.value.status_code == 404


def test_get_rides_returns_list():
    db = MagicMock()
    rides = [MagicMock(id=1), MagicMock(id=2)]
    db.query.return_value.all.return_value = rides

    result = get_rides(db)

    assert len(result) == 2


def test_update_ride_success():
    db = MagicMock()
    ride = MagicMock(status='created')

    db.query.return_value.filter.return_value.first.return_value = ride

    result = update_ride(1, 'completed', db)

    assert result.status == 'completed'
    db.commit.assert_called_once()


def test_update_ride_not_found():
    db = MagicMock()
    db.query.return_value.filter.return_value.first.return_value = None

    with pytest.raises(HTTPException):
        update_ride(999, 'completed', db)


def test_delete_ride_success():
    db = MagicMock()
    ride = MagicMock()

    db.query.return_value.filter.return_value.first.return_value = ride

    result = delete_ride(1, db)

    assert result['message'] == 'deleted'
    db.delete.assert_called_once_with(ride)


def test_delete_ride_not_found():
    db = MagicMock()
    db.query.return_value.filter.return_value.first.return_value = None

    with pytest.raises(HTTPException):
        delete_ride(999, db)


def test_ride_create_negative_price_validation():
    with pytest.raises(Exception):
        RideCreate(
            pickup='A',
            destination='B',
            price=-100,
            user_id=1,
            driver_id=1,
            tariff_id=1
        )
