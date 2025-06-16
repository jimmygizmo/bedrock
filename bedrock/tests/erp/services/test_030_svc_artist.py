import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from magma.erp.services.artist import (
    get_artist_service,
    get_artists_service,
    create_artist_service,
    update_artist_service,
    delete_artist_service,
)
from magma.erp.schemas.artist import ArtistCreate, ArtistUpdate


# TODO: DEV/TEST NEEDS A CUSTOM URL. This will come from config or the new settings module. Hardcoded here temporarily:
DEV_STACK_DATABASE_URL: str = f"postgresql+asyncpg://bedrock:bedrock@localhost:45432/bedrockdb"


# TODO: Since this is an asynchronous FastAPI application and stack, using PyTest fixtures for database sessions
#   behaves a little bit differently. This file currently uses a workaround for database connections/sessions in which
#   each individual test function establishes and tears down its own session. Prior to finding a solution to using a
#   shared session (PyTest fixture) under asynchronous conditions, this will work fine and it only requires four lines
#   of code in each function. If you have a large number of these, you might need to adjust connection pool options,
#   but any issues like that should be minor. The problem we were having with sharing the session fixture under async
#   is that we had overlap of operations with one still awaiting while another starts a new op on the same session.
#   We also had issues of which event loop was being used. I could successfully run only ONE of the below test
#   functions in this file and as soon as I added a second, we got the errors from simultaneous use of the session.
#   Most common error was:
#       sqlalchemy.exc.InterfaceError: cannot perform operation: another operation is in progress
#   Another error which came from troubleshooting variations was:
#       RuntimeError: Task ... got Future <Future pending ...> attached to a different loop
#
#   TODO: Future goals for when the fixture or equivelnt is working under async:
#         1. Clean rollback or truncate after each test.
#         2. In a separate strategy from using the Chinook seed data for testing, wipe the DB and do a new
#              create_all for every test (for tests which create their own data etc.)
#
# There is no big urgency with these fixture issues. We can have totally effective unit tests with the
# workaround technique we employ below, using individual sessions inside each test function.


@pytest.mark.asyncio
async def test_AA_svc_get_artist_existing():
    engine = create_async_engine(DEV_STACK_DATABASE_URL, echo=False)
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    async with async_session() as session:
        artist = await get_artist_service(session, 1)
        assert artist is not None
        assert artist.name == "AC/DC"


@pytest.mark.asyncio
async def test_AB_svc_get_artist_nonexistent():
    engine = create_async_engine(DEV_STACK_DATABASE_URL, echo=False)
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    async with async_session() as session:
        artist = await get_artist_service(session, 999999)
        assert artist is None


@pytest.mark.asyncio
async def test_AD_svc_get_artists(session: AsyncSession):
    engine = create_async_engine(DEV_STACK_DATABASE_URL, echo=False)
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    async with async_session() as session:
        artists = await get_artists_service(session, skip=0, limit=10)
        assert isinstance(artists, list)
        assert len(artists) > 0


@pytest.mark.asyncio
async def test_AE_svc_create_artist(session: AsyncSession):
    engine = create_async_engine(DEV_STACK_DATABASE_URL, echo=False)
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    async with async_session() as session:
        artist_in = ArtistCreate(name="UnitTest Band")
        new_artist = await create_artist_service(session, artist_in)
        assert new_artist.artist_id is not None
        assert new_artist.name == "UnitTest Band"


@pytest.mark.asyncio
async def test_AF_svc_update_artist(session: AsyncSession):
    engine = create_async_engine(DEV_STACK_DATABASE_URL, echo=False)
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    async with async_session() as session:
        artist_in = ArtistCreate(name="Temporary Artist")
        artist = await create_artist_service(session, artist_in)

        update = ArtistUpdate(name="Updated Artist")
        updated = await update_artist_service(session, artist.artist_id, update)
        assert updated is not None
        assert updated.name == "Updated Artist"


@pytest.mark.asyncio
async def test_AG_svc_delete_artist(session: AsyncSession):
    engine = create_async_engine(DEV_STACK_DATABASE_URL, echo=False)
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    async with async_session() as session:
        artist_in = ArtistCreate(name="Delete Me")
        artist = await create_artist_service(session, artist_in)

        deleted = await delete_artist_service(session, artist.artist_id)
        assert deleted is True

        post_delete = await get_artist_service(session, artist.artist_id)
        assert post_delete is None


@pytest.mark.asyncio
async def test_AH_svc_delete_nonexistent_artist(session: AsyncSession):
    engine = create_async_engine(DEV_STACK_DATABASE_URL, echo=False)
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    async with async_session() as session:
        deleted = await delete_artist_service(session, 999999)
        assert deleted is False

