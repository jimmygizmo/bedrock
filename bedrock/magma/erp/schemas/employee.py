from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from datetime import datetime
from magma.validators.shared import validate_alnum_with_spaces


# ########    PYDANTIC SCHEMA:  employee    ########


# --------  CONFIG  --------
class ConfigBase(BaseModel):
    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
    }


# --------  BASE  --------
class EmployeeBase(ConfigBase):
    last_name: Optional[str] = Field(None, alias="LastName", max_length=20)
    first_name: Optional[str] = Field(None, alias="FirstName", max_length=20)
    title: Optional[str] = Field(None, alias="Title", max_length=30)
    reports_to: Optional[int] = Field(None, alias="ReportsTo")
    birth_date: Optional[datetime] = Field(None, alias="BirthDate")
    hire_date: Optional[datetime] = Field(None, alias="HireDate")
    address: Optional[str] = Field(None, alias="Address", max_length=70)
    city: Optional[str] = Field(None, alias="City", max_length=40)
    state: Optional[str] = Field(None, alias="State", max_length=40)
    country: Optional[str] = Field(None, alias="Country", max_length=40)
    postal_code: Optional[str] = Field(None, alias="PostalCode", max_length=10)
    phone: Optional[str] = Field(None, alias="Phone", max_length=24)
    fax: Optional[str] = Field(None, alias="Fax", max_length=24)
    email: Optional[EmailStr] = Field(None, alias="Email")


# --------  CREATE (POST)  --------
class EmployeeCreate(EmployeeBase):
    last_name: str = Field(..., alias="LastName", max_length=20)
    first_name: str = Field(..., alias="FirstName", max_length=20)

    @classmethod
    @field_validator("last_name", "first_name", "title")
    def v_name_alnum_with_spaces(cls, v: Optional[str], field) -> Optional[str]:
        return validate_alnum_with_spaces(v, f"Employee.{field.name}")


# --------  UPDATE (PUT)  --------
class EmployeeUpdate(EmployeeBase):
    @classmethod
    @field_validator("last_name", "first_name", "title")
    def v_name_alnum_with_spaces(cls, v: Optional[str], field) -> Optional[str]:
        return validate_alnum_with_spaces(v, f"Employee.{field.name}")


# --------  READ (GET)  --------
class EmployeeRead(ConfigBase):
    employee_id: int = Field(..., alias="EmployeeId")
    last_name: str = Field(..., alias="LastName")
    first_name: str = Field(..., alias="FirstName")
    title: Optional[str] = Field(None, alias="Title")
    reports_to: Optional[int] = Field(None, alias="ReportsTo")
    birth_date: Optional[datetime] = Field(None, alias="BirthDate")
    hire_date: Optional[datetime] = Field(None, alias="HireDate")
    address: Optional[str] = Field(None, alias="Address")
    city: Optional[str] = Field(None, alias="City")
    state: Optional[str] = Field(None, alias="State")
    country: Optional[str] = Field(None, alias="Country")
    postal_code: Optional[str] = Field(None, alias="PostalCode")
    phone: Optional[str] = Field(None, alias="Phone")
    fax: Optional[str] = Field(None, alias="Fax")
    email: Optional[EmailStr] = Field(None, alias="Email")


# --------  REFERENCE  --------
# NOTE: In this employee table we have changed from the original schema and made all date/time TIMEZONE AWARE.
# NOTE: Bedrock does not use raw SQL for DB init. SQLAlchemy models are used. This SQL is only here for reference.
# CREATE TABLE employee
# (
#     employee_id INT NOT NULL GENERATED ALWAYS AS IDENTITY,
#     last_name VARCHAR(20) NOT NULL,
#     first_name VARCHAR(20) NOT NULL,
#     title VARCHAR(30),
#     reports_to INT,
#     birth_date TIMESTAMP,
#     hire_date TIMESTAMP,
#     address VARCHAR(70),
#     city VARCHAR(40),
#     state VARCHAR(40),
#     country VARCHAR(40),
#     postal_code VARCHAR(10),
#     phone VARCHAR(24),
#     fax VARCHAR(24),
#     email VARCHAR(60),
#     CONSTRAINT employee_pkey PRIMARY KEY  (employee_id)
# );

