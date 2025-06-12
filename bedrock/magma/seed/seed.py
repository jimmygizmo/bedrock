import json
from pathlib import Path
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from magma.core.logger import log
from magma.erp.models.genre import Genre
from magma.erp.models.media_type import MediaType
from magma.erp.models.artist import Artist
from magma.erp.models.album import Album
from magma.erp.models.track import Track
from magma.erp.schemas.genre import GenreCreate
from magma.erp.schemas.media_type import MediaTypeCreate
from magma.erp.schemas.artist import ArtistCreate
from magma.erp.schemas.album import AlbumCreate
from magma.erp.schemas.track import TrackCreate
import csv


async def load_genres(session: AsyncSession, file_path: str):
    """
    Load genre data from a CSV file into the database with Pydantic validation.
    """
    log.info(f"🔄 Loading genres from {file_path}")

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
                # Validate input row using Pydantic
                validated = GenreCreate(**row)

                # Convert validated object to SQLAlchemy model
                genre = Genre(**validated.model_dump())
                session.add(genre)
                count += 1
            except ValidationError as ve:
                errors += 1
                log.warning(f"⚠️ Validation error on row {row_num}: {ve.errors()}")
            except Exception as e:
                errors += 1
                log.error(f"❌ Unexpected error on row {row_num}: {e}")

        await session.commit()
        log.info(f"✅ {count} genres loaded successfully. {errors} row(s) had issues.")


async def load_media_types(session: AsyncSession, file_path: str):
    """
    Load media_type data from a CSV file into the database with Pydantic validation.
    """
    log.info(f"🔄 Loading media_types from {file_path}")

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
                # Validate input row using Pydantic
                validated = MediaTypeCreate(**row)

                # Convert validated object to SQLAlchemy model
                media_type = MediaType(**validated.model_dump())
                session.add(media_type)
                count += 1
            except ValidationError as ve:
                errors += 1
                log.warning(f"⚠️ Validation error on row {row_num}: {ve.errors()}")
            except Exception as e:
                errors += 1
                log.error(f"❌ Unexpected error on row {row_num}: {e}")

        await session.commit()
        log.info(f"✅ {count} media_types loaded successfully. {errors} row(s) had issues.")


async def load_artists(session: AsyncSession, file_path: str):
    """
    Load artist data from a CSV file into the database with Pydantic validation.
    """
    log.info(f"🔄 Loading artists from {file_path}")

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
                # Validate input row using Pydantic
                validated = ArtistCreate(**row)

                # Convert validated object to SQLAlchemy model
                artist = Artist(**validated.model_dump())
                session.add(artist)
                count += 1
            except ValidationError as ve:
                errors += 1
                log.warning(f"⚠️ Validation error on row {row_num}: {ve.errors()}")
            except Exception as e:
                errors += 1
                log.error(f"❌ Unexpected error on row {row_num}: {e}")

        await session.commit()
        log.info(f"✅ {count} artists loaded successfully. {errors} row(s) had issues.")


async def load_albums(session: AsyncSession, file_path: str):
    """
    Load album data from a CSV file into the database with Pydantic validation.
    """
    log.info(f"🔄 Loading albums from {file_path}")

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
                # Validate input row using Pydantic
                validated = AlbumCreate(**row)

                # Convert validated object to SQLAlchemy model
                album = Album(**validated.model_dump())
                session.add(album)
                count += 1
            except ValidationError as ve:
                errors += 1
                log.warning(f"⚠️ Validation error on row {row_num}: {ve.errors()}")
            except Exception as e:
                errors += 1
                log.error(f"❌ Unexpected error on row {row_num}: {e}")

        await session.commit()
        log.info(f"✅ {count} albums loaded successfully. {errors} row(s) had issues.")


async def load_tracks(session: AsyncSession, file_path: str):
    """
    Load track data from a CSV file into the database with Pydantic validation.
    """
    log.info(f"🔄 Loading tracks from {file_path}")

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
                # Validate input row using Pydantic
                validated = TrackCreate(**row)

                # Convert validated object to SQLAlchemy model
                track = Track(**validated.model_dump())
                session.add(track)
                count += 1
            except ValidationError as ve:
                errors += 1
                log.warning(f"⚠️ Validation error on row {row_num}: {ve.errors()}")
            except Exception as e:
                errors += 1
                log.error(f"❌ Unexpected error on row {row_num}: {e}")

        await session.commit()
        log.info(f"✅ {count} tracks loaded successfully. {errors} row(s) had issues.")

