import pytest
from fastapi import HTTPException
from unittest.mock import MagicMock, patch

from app.auth import hash_password, verify_password, create_access_token
from app.routers.auth import register, login
from app.schemas import UserCreate


def test_hash_password_and_verify():
    password = 'secret123'
    hashed = hash_password(password)

    assert hashed != password
    assert verify_password(password, hashed) is True
    assert verify_password('wrong-password', hashed) is False


def test_create_access_token_returns_string():
    token = create_access_token({'sub': 'user@test.com'})

    assert isinstance(token, str)
    assert len(token) > 20


def test_register_success():
    db = MagicMock()
    db.query.return_value.filter.return_value.first.return_value = None

    user = UserCreate(email='new@test.com', password='123456')

    result = register(user, db)

    assert result['message'] == 'registered'
    db.add.assert_called_once()
    db.commit.assert_called_once()


def test_register_existing_email():
    db = MagicMock()
    db.query.return_value.filter.return_value.first.return_value = object()

    user = UserCreate(email='exists@test.com', password='123456')

    with pytest.raises(HTTPException) as exc:
        register(user, db)

    assert exc.value.status_code == 400
    assert 'Email already exists' in exc.value.detail


def test_register_rollbacks_on_error():
    db = MagicMock()
    db.query.return_value.filter.return_value.first.return_value = None
    db.add.side_effect = Exception('db error')

    user = UserCreate(email='rollback@test.com', password='123456')

    with pytest.raises(Exception):
        register(user, db)

    db.rollback.assert_called_once()


@patch('app.routers.auth.verify_password', return_value=True)
@patch('app.routers.auth.create_access_token', return_value='fake-token')
def test_login_success(mock_token, mock_verify):
    db = MagicMock()
    db_user = MagicMock(password='hashed')
    db.query.return_value.filter.return_value.first.return_value = db_user

    user = UserCreate(email='login@test.com', password='123456')

    result = login(user, db)

    assert result['access_token'] == 'fake-token'


def test_login_user_not_found():
    db = MagicMock()
    db.query.return_value.filter.return_value.first.return_value = None

    user = UserCreate(email='missing@test.com', password='123456')

    with pytest.raises(HTTPException) as exc:
        login(user, db)

    assert exc.value.status_code == 401


@patch('app.routers.auth.verify_password', return_value=False)
def test_login_invalid_password(mock_verify):
    db = MagicMock()
    db_user = MagicMock(password='hashed')
    db.query.return_value.filter.return_value.first.return_value = db_user

    user = UserCreate(email='user@test.com', password='wrong')

    with pytest.raises(HTTPException) as exc:
        login(user, db)

    assert exc.value.status_code == 401
