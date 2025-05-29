import pytest
from pydantic import ValidationError
from magma.schemas.user import UserCreate, UserRead


# MATCH VALID RESULT - Valid input should create a UserCreate instance
def test_valid_user_create():
    user = UserCreate(
        username="testuser",
        email="test@example.com",
        password="securePass123",
        full_name="TestUser"
    )
    assert user.username == "testuser"


# ERROR EXPECTED - test_invalid_email_raises
def test_invalid_email_raises():
    with pytest.raises(ValidationError) as exc_info:
        UserCreate(
            email="not-an-email",  # invalid email format
            username="testuser",
            password="strongpassword123"
        )
    assert "value is not a valid email address" in str(exc_info.value)


# ERROR EXPECTED - Username too short
def test_username_too_short():
    with pytest.raises(ValidationError) as exc:
        UserCreate(
            username="ab",  # 2 chars is too short for the minimum of 3
            email="test@example.com",
            password="securePass123",
            full_name="TestUser"
        )
    assert "should have at least 3 characters" in str(exc.value)


# ERROR EXPECTED - Password too short
def test_password_too_short():
    with pytest.raises(ValidationError):
        UserCreate(
            username="validuser",
            email="test@example.com",
            password="123",  # 3 characters is too short for the minimum of 8
            full_name="TestUser"
        )


# ERROR EXPECTED - Extra field is forbidden    (Tests model_config setting extra="forbid")
def test_extra_field_forbidden():
    with pytest.raises(ValidationError):
        UserCreate(
            username="validuser",
            email="test@example.com",
            password="securePass123",
            full_name="TestUser",
            unknown_field="should not be allowed"  # unknown, unexpected and therefore insecure/bad
        )

