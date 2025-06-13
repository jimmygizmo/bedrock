#! /usr/bin/env python

# Platform
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select, func  # Used to detect the need to seed the database
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
# Magma application
import magma.core.config as cfg
from magma.core.logger import log
from magma.core.database import async_engine, Base
# Routers
from magma.routers import users
from magma.erp.routers import genres
# Models for seeding
from magma.erp.models.genre import Genre
from magma.erp.models.media_type import MediaType
from magma.erp.models.artist import Artist
from magma.erp.models.album import Album  # Album is only table checked to decide if the DB needs to be seeded
from magma.erp.models.track import Track
from magma.erp.models.employee import Employee
# Schemas for seeding
from magma.erp.schemas.genre import GenreCreate
from magma.erp.schemas.media_type import MediaTypeCreate
from magma.erp.schemas.artist import ArtistCreate
from magma.erp.schemas.album import AlbumCreate
from magma.erp.schemas.track import TrackCreate
from magma.erp.schemas.employee import EmployeeCreate
from magma.seed.seed import load_csv


# ########  ENTRYPOINT: Bedrock Platform - FastAPI Application Module:  magma  ########


log.info("🔥🔥🔥  BEDROCK MAGMA STARTING  🔥🔥🔥")

app = None  # Ensures global scope visibility for guvicorn

if cfg.stack_env == 'DEVELOPMENT':
    app = FastAPI()
    log.info(f"⚠️  Swagger/OpenAPI/ReDoc enabled.  Danger!!!  ⛔ DEVELOPMENT ⛔  - "
          f"cfg.stack_env: {cfg.stack_env}")
else:
    app = FastAPI(openapi_url=None, docs_url=None, redoc_url=None)
    log.info(f"⚠️  Swagger/OpenAPI/ReDoc NOT ENABLED.  SAFE FOR:  🍀 PRODUCTION 🍀  - "
             f"cfg.stack_env: {cfg.stack_env}")


# ########  MIDDLEWARE  ########

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:44443",
        "http://bedrock-local:3000",
        "http://bedrock-local:44443",
    ],
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all HTTP headers
)


# ########  ROUTERS  ########

app.include_router(users.router)  # Users
app.include_router(genres.router)  # Genres


# ########  ROOT API HANDLERS  ########

@app.get("/")
async def root():
    return {"message": "This is the root/default app in Bedrock 'Magma' FastAPI application."}


# ########  EVENT HANDLERS  ########

@app.on_event("startup")  # Deprecated but still useful
async def on_startup():
    log.debug(f"🚀  Running:  DB CREATE_ALL  (via startup event)  🚀")
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    AsyncSessionLocal = sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    # Automatic data seeding
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(func.count()).select_from(Album))
        row_count = result.scalar()
        if row_count == 0:
            log.warn("⚠️  Album (albums) table is empty!!!  Seeding all ERP (Chinook) mock data...")
            log.warn("⚠️️  IMPORTANT!  ⛔  PLEASE WAIT UNTIL DATA LOADING COMPLETES IN A FEW MINUTES  ⛔")
            # Loading in depdendency order (children first). See table dependency comments at the end of this file.
            await load_csv(
                    session,
                    model_name='genre',
                    file_path="data/chinook/Genre.csv",
                    pydantic_create_schema=GenreCreate,
                    sqlalchemy_model=Genre,
                )
            await load_csv(
                    session,
                    model_name='media_type',
                    file_path="data/chinook/MediaType.csv",
                    pydantic_create_schema=MediaTypeCreate,
                    sqlalchemy_model=MediaType,
                )
            await load_csv(
                    session,
                    model_name='artist',
                    file_path="data/chinook/Artist.csv",
                    pydantic_create_schema=ArtistCreate,
                    sqlalchemy_model=Artist,
                )
            await load_csv(
                    session,
                    model_name='album',
                    file_path="data/chinook/Album.csv",
                    pydantic_create_schema=AlbumCreate,
                    sqlalchemy_model=Album,
                )
            await load_csv(
                    session,
                    model_name='track',
                    file_path="data/chinook/Track.csv",
                    pydantic_create_schema=TrackCreate,
                    sqlalchemy_model=Track,
                )
            await load_csv(
                    session,
                    model_name='employee',
                    file_path="data/chinook/Employee.csv",
                    pydantic_create_schema=EmployeeCreate,
                    sqlalchemy_model=Employee,
                )

            # await load_customers(session, file_path="data/chinook/Customer.csv")
            # await load_invoices(session, file_path="data/chinook/Invoice.csv")
            # await load_invoice_lines(session, file_path="data/chinook/InvoiceLine.csv")
            # await load_playlists(session, file_path="data/chinook/Playlist.csv")
            # await load_playlist_tracks(session, file_path="data/chinook/PlaylistTrack.csv")
        else:
            log.info(f"Album (albums) table already has {row_count} rows. Skipping seed.")


# Based on relationships in the well-known Chinook DB schema, we must load the CSV mock data in the
# correct child-parent order of dependency. This is the order configured above:
# 1.   Genre
# 2.   MediaType
# 3.   Artist
# 4.   Album (depends on Artist)
# 5.   Track (depends on Album, Genre, MediaType)
# 6.   Employee (self-referencing for ReportsTo)
# 7.   Customer (depends on Employee via SupportRepId)
# 8.   Invoice (depends on Customer)
# 9.   InvoiceLine (depends on Invoice, Track)
# 10.  Playlist
# 11.  PlaylistTrack (depends on Playlist, Track)

