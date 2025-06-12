from typing import Optional


# ########    VALIDATORS - SHARED    ########


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# Validates alphanumeric with spaces while eliminating excess spaces and returns a valid string or errors
def validate_alnum_with_spaces(v: Optional[str], field_name: str) -> Optional[str]:
    if v is not None:
        v = v.strip()  # For 'only whitespace' and 'whitespace on ends'. 2 unwanted edge cases stripped/deleted here.
        if not v.replace(" ", "").isalnum():  # Deleting spaces pre-check here --> allows spaces.
            raise ValueError(f"Field '{field_name}' must be alphanumeric (spaces allowed)")
    return v

# USAGE EXAMPLE:
# from magma.validators.shared import validate_alnum_with_spaces
#
# @classmethod
# @field_validator('name')
# def name_alphanumeric(cls, v: Optional[str]) -> Optional[str]:
#     return validate_alnum_with_spaces(v, "Artist.name")


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # TODO: complete and implement using this example
    # Example validator placeholder
    # @classmethod
    # @field_validator('name')
    # def name_is_valid(cls, v: str) -> str:
    #     if not v or not v.strip():
    #         raise ValueError("Track name cannot be empty.")
    #     return v


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # TODO: complete and implement using this example
    # @classmethod
    # @field_validator('name')
    # def name_alphanumeric(cls, v: Optional[str]) -> Optional[str]:
    #     if v is not None and not v.replace(" ", "").isalnum():
    #         raise ValueError("Field 'name' must be alphanumeric (spaces allowed)")
    #     return v


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

