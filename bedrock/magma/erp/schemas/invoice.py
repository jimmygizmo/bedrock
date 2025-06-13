from pydantic import BaseModel, Field, field_validator, condecimal
from typing import Optional
from datetime import datetime
from magma.validators.shared import validate_alnum_with_spaces


# ########    PYDANTIC SCHEMA:  invoice    ########


# --------  CONFIG  --------
class ConfigBase(BaseModel):
    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
    }


# --------  BASE  --------
class InvoiceBase(ConfigBase):
    customer_id: Optional[int] = Field(None, alias="CustomerId")
    invoice_date: Optional[datetime] = Field(None, alias="InvoiceDate")
    billing_address: Optional[str] = Field(None, alias="BillingAddress", max_length=70)
    billing_city: Optional[str] = Field(None, alias="BillingCity", max_length=40)
    billing_state: Optional[str] = Field(None, alias="BillingState", max_length=40)
    billing_country: Optional[str] = Field(None, alias="BillingCountry", max_length=40)
    billing_postal_code: Optional[str] = Field(None, alias="BillingPostalCode", max_length=10)
    total: Optional[condecimal(max_digits=10, decimal_places=2)] = Field(None, alias="Total")


# --------  CREATE (POST)  --------
class InvoiceCreate(InvoiceBase):
    customer_id: int = Field(..., alias="CustomerId")
    invoice_date: datetime = Field(..., alias="InvoiceDate")
    total: condecimal(max_digits=10, decimal_places=2) = Field(..., alias="Total")

    @classmethod
    @field_validator("billing_address", "billing_city", "billing_state", "billing_country")
    def v_billing_alnum_with_spaces(cls, v: Optional[str], field) -> Optional[str]:
        return validate_alnum_with_spaces(v, f"Invoice.{field.name}")


# --------  UPDATE (PUT)  --------
class InvoiceUpdate(InvoiceBase):
    @classmethod
    @field_validator("billing_address", "billing_city", "billing_state", "billing_country")
    def v_billing_alnum_with_spaces(cls, v: Optional[str], field) -> Optional[str]:
        return validate_alnum_with_spaces(v, f"Invoice.{field.name}")


# --------  READ (GET)  --------
class InvoiceRead(ConfigBase):
    invoice_id: int = Field(..., alias="InvoiceId")
    customer_id: int = Field(..., alias="CustomerId")
    invoice_date: datetime = Field(..., alias="InvoiceDate")
    billing_address: Optional[str] = Field(None, alias="BillingAddress")
    billing_city: Optional[str] = Field(None, alias="BillingCity")
    billing_state: Optional[str] = Field(None, alias="BillingState")
    billing_country: Optional[str] = Field(None, alias="BillingCountry")
    billing_postal_code: Optional[str] = Field(None, alias="BillingPostalCode")
    total: condecimal(max_digits=10, decimal_places=2) = Field(..., alias="Total")


# --------  REFERENCE  --------
# NOTE: Bedrock does not use raw SQL for DB init. SQLAlchemy models are used. This SQL is only here for reference.
# CREATE TABLE invoice
# (
#     invoice_id INT NOT NULL GENERATED ALWAYS AS IDENTITY,
#     customer_id INT NOT NULL,
#     invoice_date TIMESTAMP NOT NULL,
#     billing_address VARCHAR(70),
#     billing_city VARCHAR(40),
#     billing_state VARCHAR(40),
#     billing_country VARCHAR(40),
#     billing_postal_code VARCHAR(10),
#     total NUMERIC(10,2) NOT NULL,
#     CONSTRAINT invoice_pkey PRIMARY KEY  (invoice_id)
# );

