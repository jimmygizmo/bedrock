from typing import Optional


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

