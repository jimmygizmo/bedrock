from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
from typing import Optional, List


# ########    PYDANTIC SCHEMA:  media_type    ########


# -------- Configured BaseModel --------
class ConfigBase(BaseModel):
    class Config:
        from_attributes = True
        populate_by_name = True


# -------- Base schema shared across input/output --------
class MediaTypeBase(ConfigBase):
    name: str = Field(..., alias="Name", max_length=120)


# -------- Used for incoming POST data (POST: create a new media_type with new details) --------
class MediaTypeCreate(MediaTypeBase):
    # TODO: This validation works fine when data is clean. Test it with intentionally dirty data.
    @classmethod
    @field_validator('name')
    def name_alphanumeric(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            v = v.strip()
            if not v.replace(" ", "").isalnum():
                raise ValueError("Field 'MediaType.name' must be alphanumeric (spaces allowed)")
        return v


# -------- Used for incoming POST data for *UPDATE* (PATCH/PUT: update media_type details for an existing media_type) --------
class MediaTypeUpdate(ConfigBase):
    name: Optional[str] = Field(None, alias="Name", max_length=120)


# -------- Used for response serialization (GET: /media_types/1) --------
class MediaTypeRead(ConfigBase):
    media_type_id: int
    name: str


# SQL CREATE from the original Chinook project for comparison with this Bedrock schema
#
# CREATE TABLE media_type
# (
#     media_type_id INT NOT NULL GENERATED ALWAYS AS IDENTITY,
#     name VARCHAR(120),
#     CONSTRAINT media_type_pkey PRIMARY KEY  (media_type_id)
# );

