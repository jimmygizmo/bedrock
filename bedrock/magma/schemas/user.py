from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
from typing import Optional


# ########    PYDANTIC SCHEMA:  user    ########


# -------- Base schema shared across input/output --------
# TODO: Probably make email: str = Field(..., min_length=6, max_length=60)    Research email sizes and tune 60 max.
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    full_name: Optional[str] = None


# -------- Used for incoming POST data (example: new user registration) --------
class UserCreate(UserBase):
    password: str = Field(..., min_length=8)  # Not in UserBase. Including it in UserRead via UserBase is insecure.

    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    @classmethod
    @field_validator('username')
    def username_alphanumeric(cls, v: str) -> str:
        if not v.isalnum():
            raise ValueError("Field 'username' must be alphanumeric")
        return v

    # TODO: EmailStr Pydantic type is problematic. changing to use str type and then totally custom email validation
    @classmethod
    @field_validator("email", mode="before")
    def lowercase_email(cls, v: str) -> str:
        return v.lower()


    @classmethod
    @field_validator('full_name')
    def full_name_alphanumeric(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not v.replace(" ", "").isalnum():
            raise ValueError("Field 'full_name' must be alphanumeric (spaces allowed)")
        return v

    @classmethod
    @field_validator('password')
    def strong_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.islower() for c in v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        if not any(c in "!@#$%^&*()-_=+[{]};:,<.>/?\\" for c in v):
            raise ValueError("Password must contain at least one special character")
        return v


# -------- Used for response serialization (example: API GET /users/1) --------
class UserRead(UserBase):
    id: int

    class Config:
        # orm_mode = True  # Renamed to from_attributes - below:
        from_attributes = True

