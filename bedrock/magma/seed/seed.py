import json
from pathlib import Path
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from magma.core.logger import log
from magma.models.erp.album import Album
from magma.models.erp.artist import Artist
from magma.models.erp.track import Track
from magma.schemas.album import AlbumCreate
from magma.schemas.artist import ArtistCreate
from magma.schemas.track import TrackCreate
import csv


async def load_albums(session: AsyncSession, file_path: str):
    log.info(f"🔄 Loading albums from {file_path}")
    path = Path(file_path)

    with path.open(mode="r", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            album = Album(
                album_id=int(row["AlbumId"]),
                title=row["Title"],
                artist_id=int(row["ArtistId"])
            )
            session.add(album)

    await session.commit()
    log.info("✅ Albums loaded.")


async def load_artists(session: AsyncSession, file_path: str):
    log.info(f"🔄 Loading artists from {file_path}")
    path = Path(file_path)

    with path.open(mode="r", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            artist = Artist(
                artist_id=int(row["ArtistId"]),
                name=row.get("Name")
            )
            session.add(artist)

    await session.commit()
    log.info("✅ Artists loaded.")


# async def load_tracks(session: AsyncSession, file_path: str):
#     log.info(f"🔄 Loading tracks from {file_path}")
#     path = Path(file_path)
#
#     with path.open(mode="r", encoding="utf-8") as fh:
#         reader = csv.DictReader(fh)
#         for row in reader:
#             track = Track(
#                 track_id=int(row["TrackId"]),
#                 name=row["Name"],
#                 album_id=int(row["AlbumId"]) if row["AlbumId"] else None,
#                 media_type_id=int(row["MediaTypeId"]),
#                 genre_id=int(row["GenreId"]) if row["GenreId"] else None,
#                 composer=row.get("Composer"),
#                 milliseconds=int(row["Milliseconds"]),
#                 bytes=int(row["Bytes"]) if row["Bytes"] else None,
#                 unit_price=float(row["UnitPrice"]),
#             )
#             session.add(track)
#
#     await session.commit()
#     log.info("✅ Tracks loaded.")


async def load_tracks(session: AsyncSession, file_path: str):
    """
    Load track data from a CSV file into the database with Pydantic validation.
    """
    log.info(f"Loading tracks from {file_path}")

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



