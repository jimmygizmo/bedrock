from pydantic import BaseModel, Field, condecimal
from typing import Optional
from magma.erp.schemas.track import TrackRead


# ########    PYDANTIC SCHEMA:  invoice_line    ########


# --------  CONFIG  --------
class ConfigBase(BaseModel):
    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
    }


# --------  BASE  --------
class InvoiceLineBase(ConfigBase):
    invoice_id: Optional[int] = Field(None, alias="InvoiceId")
    track_id: Optional[int] = Field(None, alias="TrackId")
    unit_price: Optional[condecimal(max_digits=10, decimal_places=2)] = Field(None, alias="UnitPrice")
    quantity: Optional[int] = Field(None, alias="Quantity")


# --------  CREATE (POST)  --------
class InvoiceLineCreate(InvoiceLineBase):
    invoice_id: int = Field(..., alias="InvoiceId")
    track_id: int = Field(..., alias="TrackId")
    unit_price: condecimal(max_digits=10, decimal_places=2) = Field(..., alias="UnitPrice")
    quantity: int = Field(..., alias="Quantity")


# --------  UPDATE (PUT)  --------
class InvoiceLineUpdate(InvoiceLineBase):
    pass


# --------  READ (GET)  --------
class InvoiceLineRead(ConfigBase):
    invoice_line_id: int = Field(..., alias="InvoiceLineId")
    invoice_id: int = Field(..., alias="InvoiceId")
    track_id: int = Field(..., alias="TrackId")
    unit_price: condecimal(max_digits=10, decimal_places=2) = Field(..., alias="UnitPrice")
    quantity: int = Field(..., alias="Quantity")

    track: Optional[TrackRead]


# --------  REFERENCE  --------
# NOTE: Bedrock does not use raw SQL for DB init. SQLAlchemy models are used. This SQL is only here for reference.
# CREATE TABLE invoice_line
# (
#     invoice_line_id INT NOT NULL GENERATED ALWAYS AS IDENTITY,
#     invoice_id INT NOT NULL,
#     track_id INT NOT NULL,
#     unit_price NUMERIC(10,2) NOT NULL,
#     quantity INT NOT NULL,
#     CONSTRAINT invoice_line_pkey PRIMARY KEY  (invoice_line_id)
# );

