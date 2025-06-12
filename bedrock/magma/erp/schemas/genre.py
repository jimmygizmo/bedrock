from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
from typing import Optional, List
from magma.validators.shared import validate_alnum_with_spaces


# ########    PYDANTIC SCHEMA:  genre    ########


# -------- Configured BaseModel --------
class ConfigBase(BaseModel):
    class Config:
        from_attributes = True
        populate_by_name = True


# -------- Base schema shared across input/output --------
class GenreBase(ConfigBase):
    name: Optional[str] = Field(None, alias="Name", max_length=120)


# -------- Used for incoming POST data (POST: create a new genre with new details) --------
class GenreCreate(GenreBase):
    # OPTION - We could enforce name being present in create by adding this override of GenreBase in the following line:
    # name: str = Field(..., alias="Name", max_length=120)  # Disabled. Here as an example. NOTE: DB allows null here.
    @classmethod
    @field_validator('name')
    def v_name_alnum_with_spaces(cls, v: Optional[str]) -> Optional[str]:
        return validate_alnum_with_spaces(v, "Genre.name")
    # def name_alphanumeric(cls, v: Optional[str]) -> Optional[str]:
    #     if v is not None:
    #         v = v.strip()
    #         if not v.replace(" ", "").isalnum():
    #             raise ValueError("Field 'Genre.name' must be alphanumeric (spaces allowed)")
    #     return v


# -------- Used for incoming POST data for *UPDATE* (PATCH/PUT: update genre details for an existing genre) --------
class GenreUpdate(ConfigBase):
    name: Optional[str] = Field(None, alias="Name", max_length=120)
    @classmethod
    @field_validator('name')
    def v_name_alnum_with_spaces(cls, v: Optional[str]) -> Optional[str]:
        return validate_alnum_with_spaces(v, "Genre.name")
    # def name_alphanumeric(cls, v: Optional[str]) -> Optional[str]:
    #     if v is not None:
    #         v = v.strip()
    #         if not v.replace(" ", "").isalnum():
    #             raise ValueError("Field 'Genre.name' must be alphanumeric (spaces allowed)")
    #     return v


# -------- Used for response serialization (GET: /genres/1) --------
class GenreRead(ConfigBase):
    genre_id: int = Field(..., alias="GenreId")
    name: str = Field(..., alias="Name")


# SQL CREATE from the original Chinook project for comparison with this Bedrock schema
#
# CREATE TABLE genre
# (
#     genre_id INT NOT NULL GENERATED ALWAYS AS IDENTITY,
#     name VARCHAR(120),
#     CONSTRAINT genre_pkey PRIMARY KEY  (genre_id)
# );

