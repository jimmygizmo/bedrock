from typing import Optional


# TODO: This is not used yet.

def validate_alphanumeric_with_spaces(v: Optional[str], field_name: str) -> Optional[str]:
    if v is not None:
        v = v.strip()
        if not v.replace(" ", "").isalnum():
            raise ValueError(f"Field '{field_name}' must be alphanumeric (spaces allowed)")
    return v

# USAGE EXAMPLE:
# from validators.shared import validate_alphanumeric_with_spaces
#
# @classmethod
# @field_validator('name')
# def name_alphanumeric(cls, v: Optional[str]) -> Optional[str]:
#     return validate_alphanumeric_with_spaces(v, "Artist.name")
