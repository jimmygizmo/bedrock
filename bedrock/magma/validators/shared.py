from typing import Optional


# ########    VALIDATORS - SHARED    ########


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# TODO: See the Employee schema for an idea to pass the field so we can use field.name instead of passing
#   field_name. One question is what is field.name? It should be variable name. Make sure it isn't the alias.
#   Probably not, but that might be OK too. It is a good refactor/abstraction and eliminates some hardcoding.
# IT LOOKS LIKE THIS on the schema side:
#     @field_validator("last_name", "first_name", "title")
#     def v_name_alnum_with_spaces_ALT(cls, v: Optional[str], field) -> Optional[str]:
#         return validate_alnum_with_spaces(v, f"Employee.{field.name}")


# Validates alphanumeric with spaces while eliminating excess spaces and returns a valid string or errors
def validate_alnum_with_spaces(v: Optional[str], field_name: str) -> Optional[str]:
    if v is not None:
        v = v.strip()  # For 'only whitespace' and 'whitespace on ends'. 2 unwanted edge cases stripped/deleted here.
        v_check = v.replace(" ", "")  # Remove space from check to allow spaces
        if not v_check.isalnum():
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

# MORE:
# def parse_optional_int_field(v, field_name):
#     if v == "" or v is None:
#         return None
#     try:
#         return int(v)
#     except ValueError:
#         raise ValueError(f"{field_name} must be an integer or blank/null")
# USE IT:
# @field_validator("ReportsTo", mode="before")
# def v_reports_to(cls, v): return parse_optional_int_field(v, "ReportsTo")

