from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
from typing import Optional, Union
from datetime import datetime
from magma.core.logger import log
from magma.validators.shared import validate_alnum_with_spaces


# ########    PYDANTIC SCHEMA:  employee    ########


# --------  CONFIG  --------
# #### This is supposed to be V2 and work but it does not. The validator still does not trigger.
class ConfigBase(BaseModel):
    # model_config = ConfigDict(from_attributes=True)
    #
    # model_config = ConfigDict(from_attributes=True, populate_by_name=True)
    #
    # model_config = ConfigDict(from_attributes=True, populate_by_name=True, extra="forbid")
    #
    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
    }

# ##### This is supposed to be V1 and not work
# class ConfigBase(BaseModel):
#     class Config:
#         from_attributes = True
#         populate_by_name = True


# --------  BASE  --------
class EmployeeBase(ConfigBase):
    last_name: Optional[str] = Field(None, alias="LastName", max_length=20)
    first_name: Optional[str] = Field(None, alias="FirstName", max_length=20)
    title: Optional[str] = Field(None, alias="Title", max_length=30)
    reports_to: Optional[int] = Field(None, alias="ReportsTo")  # '' can't get past int check to even hit validator
    # reports_to: Union[int, str, None] = Field(None, alias="ReportsTo")  # This Union allows the '' (str) to hit validator
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

    # TRYING THE VALIDATOR IN BASE
    # @classmethod
    # @field_validator("reports_to", mode="before")
    # def v_reports_to_blank_string_as_none(cls, v):
    #     log.debug(f"⛔⛔⛔⛔  INSIDE VALIDATOR v_reports_to_blank_string_as_none")
    #     if v == "" or v is None:
    #         return None
    #     return int(v)


# --------  CREATE/POST  --------
class EmployeeCreate(EmployeeBase):
    last_name: str = Field(..., alias="LastName", max_length=20)
    first_name: str = Field(..., alias="FirstName", max_length=20)

    # Chinook data has a manager with blank '' value for reports_to. This needs to be int or None to pass validation so
    # we need to 'validate' it by converting empty string to literal None. TODO: Consider this for update?
    # TODO: If we consider such a converter validator for update here, it starts to look like something we might need
    #   in numerous places. This requires further analysis but the answer will become obvious soon enough.
    #   See validators.py for an example of a generalized version of this validator with usage example.


    @classmethod
    @field_validator("reports_to", mode="before")
    def v_reports_to_blank_string_as_none(cls, v):
        log.debug(f"⛔⛔⛔⛔  INSIDE VALIDATOR v_reports_to_blank_string_as_none")
        if v == "" or v is None:
            return None
        return int(v)


    # TODO: FAILING TO RUN. Triggers neither for "reports_to" nor for "ReportsTo". Because of this, currently one of
    #   our rows of EMployee.csv data will not load. The error is:
    #   Validation error on row 1: [{'type': 'int_parsing', 'loc': ('ReportsTo',),
    #   'msg': 'Input should be a valid integer, unable to parse string as an integer', 'input': '',
    #   'url': 'https://errors.pydantic.dev/2.11/v/int_parsing'}]


    # @classmethod
    # @field_validator("last_name", "first_name", "title")
    # def v_name_alnum_with_spaces_ALT(cls, v: Optional[str], field) -> Optional[str]:
    #     return validate_alnum_with_spaces(v, f"Employee.{field.name}")
    #
    # NOTE: THIS IS A NEW ALT FORMAT THAT PASSES THE FIELD ARGUMENT SO WE CAN USE field.name
    # TODO: Assess then likely modify the validators to all do this. Elimnates a little hard-coding.


# --------  UPDATE/PUT  --------
class EmployeeUpdate(EmployeeBase):
    @classmethod
    @field_validator("last_name", "first_name", "title")
    def v_name_alnum_with_spaces_ALT(cls, v: Optional[str], field) -> Optional[str]:
        return validate_alnum_with_spaces(v, f"Employee.{field.name}")


# --------  READ/GET  --------
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

