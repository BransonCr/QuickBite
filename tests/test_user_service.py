from unittest.mock import patch

import pytest
from fastapi import HTTPException

from app.schemas.User import User, UserCreate, UserRole, UserUpdate
from app.services.UserService import UserService


def make_user(user_id="abc-123"):
    return User(
        user_id=user_id,
        username="testuser",
        email="test@example.com",
        password_hash="hashed",
        phone="1234567890",
        role=UserRole.CUSTOMER,
        location="123 Main St",
        postal_code="V1V1V1",
        created_at="2026-01-01",
    )


def make_user_create():
    return UserCreate(
        username="testuser",
        email="test@example.com",
        password_hash="hashed",
        phone="1234567890",
        role=UserRole.CUSTOMER,
        location="123 Main St",
        postal_code="V1V1V1",
        created_at="2026-01-01",
    )


@patch("app.services.UserService.save_all")
@patch("app.services.UserService.load_all")
def test_get_users(mock_load, mock_save):
    mock_load.return_value = [make_user()]
    service = UserService()
    result = service.get_users()
    assert len(result) == 1
    assert result[0].username == "testuser"


@patch("app.services.UserService.save_all")
@patch("app.services.UserService.load_all")
def test_get_user_found(mock_load, mock_save):
    mock_load.return_value = [make_user("abc-123")]
    service = UserService()
    result = service.get_user("abc-123")
    assert result.user_id == "abc-123"


@patch("app.services.UserService.save_all")
@patch("app.services.UserService.load_all")
def test_get_user_not_found(mock_load, mock_save):
    mock_load.return_value = []
    service = UserService()
    with pytest.raises(HTTPException) as exc:
        service.get_user("does-not-exist")
    assert exc.value.status_code == 404


@patch("app.services.UserService.save_all")
@patch("app.services.UserService.load_all")
def test_create_user(mock_load, mock_save):
    mock_load.return_value = []
    service = UserService()
    result = service.create_user(make_user_create())
    assert result.username == "testuser"
    assert result.user_id is not None
    mock_save.assert_called_once()


@patch("app.services.UserService.save_all")
@patch("app.services.UserService.load_all")
def test_update_user(mock_load, mock_save):
    mock_load.return_value = [make_user("abc-123")]
    service = UserService()
    update = UserUpdate(
        username="updated",
        email="updated@example.com",
        password_hash="newhash",
        phone="0987654321",
        role=UserRole.ADMIN,
        location="456 Other St",
        postal_code="V2V2V2",
    )
    result = service.update_user("abc-123", update)
    assert result.username == "updated"
    mock_save.assert_called_once()


@patch("app.services.UserService.save_all")
@patch("app.services.UserService.load_all")
def test_update_user_not_found(mock_load, mock_save):
    mock_load.return_value = []
    service = UserService()
    with pytest.raises(HTTPException) as exc:
        service.update_user(
            "does-not-exist",
            UserUpdate(
                username="x",
                email="x@x.com",
                password_hash="x",
                phone="x",
                role=UserRole.CUSTOMER,
                location="x",
                postal_code="x",
            ),
        )
    assert exc.value.status_code == 404


@patch("app.services.UserService.save_all")
@patch("app.services.UserService.load_all")
def test_delete_user(mock_load, mock_save):
    mock_load.return_value = [make_user("abc-123")]
    service = UserService()
    service.delete_user("abc-123")
    mock_save.assert_called_once()


@patch("app.services.UserService.save_all")
@patch("app.services.UserService.load_all")
def test_delete_user_not_found(mock_load, mock_save):
    mock_load.return_value = []
    service = UserService()
    with pytest.raises(HTTPException) as exc:
        service.delete_user("does-not-exist")
    assert exc.value.status_code == 404
