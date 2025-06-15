from pydantic import BaseModel, Field, field_validator
from typing import Optional
from magma.validators.shared import validate_alnum_with_spaces


# ########    PYDANTIC SCHEMA:  media_type    ########


# --------  CONFIG  --------
class ConfigBase(BaseModel):
    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
    }


# --------  BASE  --------
class MediaTypeBase(ConfigBase):
    name: Optional[str] = Field(None, alias="Name", max_length=120)


# --------  CREATE (POST)  --------
class MediaTypeCreate(MediaTypeBase):
    # OPTION - We could enforce name being present in create by adding this override of MediaTypeBase in the following line:
    # name: str = Field(..., alias="Name", max_length=120)  # Disabled. Here as an example. NOTE: DB allows null here.
    @classmethod
    @field_validator('name')
    def v_name_alnum_with_spaces(cls, v: Optional[str]) -> Optional[str]:
        return validate_alnum_with_spaces(v, "MediaType.name")


# --------  UPDATE (PUT)  --------
class MediaTypeUpdate(ConfigBase):
    name: Optional[str] = Field(None, alias="Name", max_length=120)
    @classmethod
    @field_validator('name')
    def v_name_alnum_with_spaces(cls, v: Optional[str]) -> Optional[str]:
        return validate_alnum_with_spaces(v, "MediaType.name")


# --------  READ (GET)  --------
class MediaTypeRead(ConfigBase):
    media_type_id: int = Field(..., alias="MediaTypeId")
    name: str = Field(..., alias="Name")


# --------  REFERENCE  --------
# NOTE: Bedrock does not use raw SQL for DB init. SQLAlchemy models are used. This SQL is only here for reference.
# CREATE TABLE media_type
# (
#     media_type_id INT NOT NULL GENERATED ALWAYS AS IDENTITY,
#     name VARCHAR(120),
#     CONSTRAINT media_type_pkey PRIMARY KEY  (media_type_id)
# );

