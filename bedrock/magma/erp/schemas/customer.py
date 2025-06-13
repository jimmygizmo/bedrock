from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from magma.validators.shared import validate_alnum_with_spaces


# ########    PYDANTIC SCHEMA:  customer    ########


# --------  CONFIG  --------
class ConfigBase(BaseModel):
    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
    }


# --------  BASE  --------
class CustomerBase(ConfigBase):
    first_name: Optional[str] = Field(None, alias="FirstName", max_length=40)
    last_name: Optional[str] = Field(None, alias="LastName", max_length=20)
    company: Optional[str] = Field(None, alias="Company", max_length=80)
    address: Optional[str] = Field(None, alias="Address", max_length=70)
    city: Optional[str] = Field(None, alias="City", max_length=40)
    state: Optional[str] = Field(None, alias="State", max_length=40)
    country: Optional[str] = Field(None, alias="Country", max_length=40)
    postal_code: Optional[str] = Field(None, alias="PostalCode", max_length=10)
    phone: Optional[str] = Field(None, alias="Phone", max_length=24)
    fax: Optional[str] = Field(None, alias="Fax", max_length=24)
    email: Optional[EmailStr] = Field(None, alias="Email", max_length=60)
    support_rep_id: Optional[int] = Field(None, alias="SupportRepId")


# --------  CREATE (POST)  --------
class CustomerCreate(CustomerBase):
    first_name: str = Field(..., alias="FirstName", max_length=40)
    last_name: str = Field(..., alias="LastName", max_length=20)
    email: EmailStr = Field(..., alias="Email", max_length=60)

    @classmethod
    @field_validator("first_name", "last_name", "company", "city", "state", "country")
    def v_name_alnum_with_spaces(cls, v: Optional[str], field) -> Optional[str]:
        return validate_alnum_with_spaces(v, f"Customer.{field.name}")


# --------  UPDATE (PUT)  --------
class CustomerUpdate(CustomerBase):
    @classmethod
    @field_validator("first_name", "last_name", "company", "city", "state", "country")
    def v_name_alnum_with_spaces(cls, v: Optional[str], field) -> Optional[str]:
        return validate_alnum_with_spaces(v, f"Customer.{field.name}")


# --------  READ (GET)  --------
class CustomerRead(ConfigBase):
    customer_id: int = Field(..., alias="CustomerId")
    first_name: str = Field(..., alias="FirstName")
    last_name: str = Field(..., alias="LastName")
    company: Optional[str] = Field(None, alias="Company")
    address: Optional[str] = Field(None, alias="Address")
    city: Optional[str] = Field(None, alias="City")
    state: Optional[str] = Field(None, alias="State")
    country: Optional[str] = Field(None, alias="Country")
    postal_code: Optional[str] = Field(None, alias="PostalCode")
    phone: Optional[str] = Field(None, alias="Phone")
    fax: Optional[str] = Field(None, alias="Fax")
    email: EmailStr = Field(..., alias="Email")
    support_rep_id: Optional[int] = Field(None, alias="SupportRepId")


# --------  REFERENCE  --------
# NOTE: Bedrock does not use raw SQL for DB init. SQLAlchemy models are used. This SQL is only here for reference.
# CREATE TABLE customer
# (
#     customer_id INT NOT NULL GENERATED ALWAYS AS IDENTITY,
#     first_name VARCHAR(40) NOT NULL,
#     last_name VARCHAR(20) NOT NULL,
#     company VARCHAR(80),
#     address VARCHAR(70),
#     city VARCHAR(40),
#     state VARCHAR(40),
#     country VARCHAR(40),
#     postal_code VARCHAR(10),
#     phone VARCHAR(24),
#     fax VARCHAR(24),
#     email VARCHAR(60) NOT NULL,
#     support_rep_id INT,
#     CONSTRAINT customer_pkey PRIMARY KEY  (customer_id)
# );

