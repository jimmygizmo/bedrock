from pathlib import Path
from typing import Type
from pydantic import BaseModel, ValidationError
from magma.core.database import Base
from sqlalchemy.ext.asyncio import AsyncSession
from magma.core.logger import log
import csv


def normalized_row(row: dict) -> dict:
    """
    Convert empty strings in a row dict to None.
    """
    return {k: (v if v != '' else None) for k, v in row.items()}


async def load_csv(
        session: AsyncSession,
        model_name: str,
        file_path: str,
        pydantic_create_schema: Type[BaseModel],
        sqlalchemy_model: Type[Base],
    ):
    """
    Load model/table data from a CSV file into the database with Pydantic validation.
    """
    log.info(f"🔄 Loading {model_name}s from {file_path}")

    path = Path(file_path)
    if not path.exists():
        log.error(f"❌ File not found: {file_path}")
        return

    with path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        count = 0
        errors = 0
        for row_num, row in enumerate(reader, start=1):
            try:
                norm_row = normalized_row(row)
                # log.debug(norm_row)
                # Validate input using dynamic Pydantic schema
                validated = pydantic_create_schema(**norm_row)

                # Convert validated_pydantic_model to SQLAlchemy model
                validated_pydantic_model = sqlalchemy_model(**validated.model_dump())

                session.add(validated_pydantic_model)
                count += 1
            except ValidationError as ve:
                errors += 1
                log.warning(f"⚠️ Validation error on row {row_num}: {ve.errors()}")
            except Exception as e:
                errors += 1
                log.error(f"❌ Unexpected error on row {row_num}: {e}")

        await session.commit()
        log.info(f"✅ {count} {model_name}s loaded successfully. {errors} row(s) had issues.")

