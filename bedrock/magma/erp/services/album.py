from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, joinedload

from magma.erp.models.album import Album
from magma.erp.models.track import Track
from magma.erp.schemas.album import AlbumCreate, AlbumUpdate

# For temporary examination of the raw SQL from select() statements
from sqlalchemy.dialects import postgresql
from magma.core.logger import log


# ########    SERVICE:  album    ########


# TODO: Add this to formal docs:
# ***  HOW TO FIGURE OUT WHEN YOU NEED THE EAGER LOADING FROM selecinload - AND WHAT YOU NEED TO EAGER LOAD  ***
# NOTE: AlbumRead includes these:
#     artist: ArtistSimpleRead
#                 class ArtistSimpleRead(ConfigBase):
#                     artist_id: int = Field(alias="ArtistId")
#                     name: str = Field(alias="Name")
#     tracks: list[TrackSimpleRead]
#                 class TrackSimpleRead(ConfigBase):
#                     track_id: int
#                     name: str
#                     media_type: Optional[MediaTypeRead]
#                     genre: Optional[GenreRead]
#                    ... other flat metadata fields ...
#
# **** HENCE - AlbumRead UNDER ASYNC ALWAYS REQUIRES:
#             selectinload(Album.artist),
#             selectinload(Album.tracks).selectinload(Track.genre),
#             selectinload(Album.tracks).selectinload(Track.media_type),


# TOPIC - HOW TO DECIDE BETWEEN JOINEDLOAD VS. SELECTIN LOAD (many more queries - Python does more work)
# joinedload for 1:1 or few children
# selectinload for large lists, or when they want better memory use per request
# JOINEDLOAD CAN BLOW UP IF YOU DONT WATCH RELATIONSHIPS AND DATA. JL SHIFTS WORK TO THE DB. FEWER, LARGER CALLS.
# TODO: There are many excellent and advanced topics touched on in the comments on this page. Document them well.
#
# GENERAL STRATEGY:
# Benchmark and profile both strategies in real usage
# Use hybrid strategies (joinedload for artist, selectinload for tracks)
# Implement custom pagination or batching when traversing large graphs
# Use explicit joins or with_entities() for read-optimized paths
# Prefer selectinload for graph breadth, joinedload for graph depth


async def get_album_service(session: AsyncSession, album_id: int) -> Album | None:
    # statement = (
    #     select(Album)
    #     .options(
    #         selectinload(Album.artist),
    #         selectinload(Album.tracks).selectinload(Track.genre),
    #         selectinload(Album.tracks).selectinload(Track.media_type),
    #     )
    #     .where(Album.album_id == album_id)
    # )
    # TRYING JOINEDLOAD TO HAVE THE DATABASE DO ALL THE WORK - RESULT SET SHOULD BE SAME - WE WILL SEE ENTIRE QUERY
    statement = (
        select(Album)
        .options(
            joinedload(Album.artist),
            joinedload(Album.tracks).joinedload(Track.genre),
            joinedload(Album.tracks).joinedload(Track.media_type),
        )
        .where(Album.album_id == album_id)
    )

    # For educational purposes, as this is probably our most complex eager load, lets see the raw SQL created
    # for this select(). We have extra imports for this noted above.
    raw_sql = statement.compile(dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True})
    log.debug(f"- - - - - - - - -  RAW SQL  - - - - - - - - -")
    log.debug(f"{raw_sql}")
    log.debug(f"- - - - - - - - - - - - - - - - - - - - - - -")

    result = await session.execute(statement)
    # album = result.scalar_one_or_none()  # FOR USE WITH THE SELECTINLOAD VERSION
    album = result.unique().scalar_one_or_none()  # FOR USE WITH THE JOINEDLOAD VERSION
    return album


# ---- EDUCATIONAL - THE ABOVE JOINEDLOAD STATEMENT HAS THIS STRUCTURE: ----
# [albums]
#   └── 1-to-1 ──► [artists]
#   └── 1-to-many ──► [tracks]
#                       └── many-to-1 ──► [genres]
#                       └── many-to-1 ──► [media_types]
#
# ---- EDUCATIONAL - HERE IS A BREAKDOWN OF THE QUERY: ----
#
# FROM albums
# LEFT OUTER JOIN tracks AS tracks_1
#   ON albums."AlbumId" = tracks_1."AlbumId"
# LEFT OUTER JOIN media_types AS media_types_1
#   ON tracks_1."MediaTypeId" = media_types_1."MediaTypeId"
# LEFT OUTER JOIN genres AS genres_1
#   ON tracks_1."GenreId" = genres_1."GenreId"
# LEFT OUTER JOIN artists AS artists_1
#   ON albums."ArtistId" = artists_1."ArtistId"
#
# ---- EDUCATIONAL - THE EXECUTION ORDER OF THIS QUERY: ----
# [albums]  ─────────────┐
#    │                   │
#    ▼                   ▼
# [tracks]         [artists]
#    │
#    ├────► [media_types]
#    │
#    └────► [genres]
#
# ---- EDUCATIONAL - SHAPE OF EACH ROW RETURNED: ----
#
# One Album
# One of its Tracks
# Track's Genre
# Track's MediaType
# Album's Artist
#


async def get_albums_service(session: AsyncSession, skip: int = 0, limit: int = 100) -> list[Album]:
    statement = (
        select(Album)
        .options(
            selectinload(Album.artist),
            selectinload(Album.tracks).selectinload(Track.genre),
            selectinload(Album.tracks).selectinload(Track.media_type),
        )
        .offset(skip)
        .limit(limit)
    )
    result = await session.execute(statement)
    albums = result.scalars().all()
    return list(albums)  # list() here does nothing but does suppress false static type warnings


async def create_album_service(session: AsyncSession, album_in: AlbumCreate) -> Album:
    album = Album(**album_in.model_dump())
    session.add(album)
    await session.commit()
    await session.refresh(album)
    statement = (
        select(Album)
        .options(
            selectinload(Album.artist),
            selectinload(Album.tracks),
        )
        .where(Album.album_id == album.album_id)
    )
    result = await session.execute(statement)
    album_with_rels = result.scalar_one()
    return album_with_rels


async def update_album_service(session: AsyncSession, album_id: int, album_in: AlbumUpdate) -> Album | None:
    album = await get_album_service(session, album_id)
    if not album:
        return None
    for field, value in album_in.model_dump(exclude_unset=True).items():
        setattr(album, field, value)
    await session.commit()
    await session.refresh(album)
    statement = (
        select(Album)
        .options(
            selectinload(Album.artist),
            selectinload(Album.tracks),
        )
        .where(Album.album_id == album.album_id)
    )
    result = await session.execute(statement)
    album_with_rels = result.scalar_one()
    return album_with_rels


async def delete_album_service(session: AsyncSession, album_id: int) -> bool:
    album = await get_album_service(session, album_id)
    if not album:
        return False

    await session.delete(album)
    await session.commit()
    return True

