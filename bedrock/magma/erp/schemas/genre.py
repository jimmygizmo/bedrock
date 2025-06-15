from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
from typing import Optional, List
from magma.validators.shared import validate_alnum_with_spaces


# ########    PYDANTIC SCHEMA:  genre    ########


# --------  CONFIG  --------
class ConfigBase(BaseModel):
    class Config:
        from_attributes = True
        populate_by_name = True


# --------  BASE  --------
class GenreBase(ConfigBase):
    name: Optional[str] = Field(None, alias="Name", max_length=120)


# --------  CREATE/POST  --------
class GenreCreate(GenreBase):
    # OPTION - We could enforce name being present in create by adding this override of GenreBase in the following line:
    # name: str = Field(..., alias="Name", max_length=120)  # Disabled. Here as an example. NOTE: DB allows null here.
    @classmethod
    @field_validator('name')
    def v_name_alnum_with_spaces(cls, v: Optional[str]) -> Optional[str]:
        return validate_alnum_with_spaces(v, "Genre.name")


# --------  UPDATE/PUT  --------
class GenreUpdate(ConfigBase):
    name: Optional[str] = Field(None, alias="Name", max_length=120)
    @classmethod
    @field_validator('name')
    def v_name_alnum_with_spaces(cls, v: Optional[str]) -> Optional[str]:
        return validate_alnum_with_spaces(v, "Genre.name")


# --------  READ/GET  --------
class GenreRead(ConfigBase):
    genre_id: int = Field(..., alias="GenreId")
    name: str = Field(..., alias="Name")


# --------  REFERENCE  --------
# NOTE: Bedrock does not use raw SQL for DB init. SQLAlchemy models are used. This SQL is only here for reference.
# CREATE TABLE genre
# (
#     genre_id INT NOT NULL GENERATED ALWAYS AS IDENTITY,
#     name VARCHAR(120),
#     CONSTRAINT genre_pkey PRIMARY KEY  (genre_id)
# );

