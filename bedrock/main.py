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
# Routers - Base
from magma.routers import users
# Routers - ERP
from magma.erp.routers import genres
from magma.erp.routers import media_types
from magma.erp.routers import artists
from magma.erp.routers import albums
from magma.erp.routers import tracks
from magma.erp.routers import employees
from magma.erp.routers import customers
from magma.erp.routers import invoices
from magma.erp.routers import invoice_lines
from magma.erp.routers import playlists
from magma.erp.routers import playlist_tracks
# Models for seeding
from magma.erp.models.genre import Genre
from magma.erp.models.media_type import MediaType
from magma.erp.models.artist import Artist
from magma.erp.models.album import Album  # Album is the only table checked to decide if the DB needs to be seeded
from magma.erp.models.track import Track
from magma.erp.models.employee import Employee
from magma.erp.models.customer import Customer
from magma.erp.models.invoice import Invoice
from magma.erp.models.invoice_line import InvoiceLine
from magma.erp.models.playlist import Playlist
from magma.erp.models.playlist_track import PlaylistTrack
# Schemas for seeding
from magma.erp.schemas.genre import GenreCreate
from magma.erp.schemas.media_type import MediaTypeCreate
from magma.erp.schemas.artist import ArtistCreate
from magma.erp.schemas.album import AlbumCreate
from magma.erp.schemas.track import TrackCreate
from magma.erp.schemas.employee import EmployeeCreate
from magma.erp.schemas.customer import CustomerCreate
from magma.erp.schemas.invoice import InvoiceCreate
from magma.erp.schemas.invoice_line import InvoiceLineCreate
from magma.erp.schemas.playlist import PlaylistCreate
from magma.erp.schemas.playlist_track import PlaylistTrackCreate
# Seeder
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

# MAIN ROUTERS
app.include_router(users.router)  # Users
# ERP ROUTERS
app.include_router(genres.router)  # Genres
app.include_router(media_types.router)  # MediaTypes
app.include_router(artists.router)  # Artists
app.include_router(albums.router)  # Albums
app.include_router(tracks.router)  # Tracks
app.include_router(employees.router)  # Employees
app.include_router(customers.router)  # Customers
app.include_router(invoices.router)  # Invoices
app.include_router(invoice_lines.router)  # InvoiceLines
app.include_router(playlists.router)  # Playlist
app.include_router(playlist_tracks.router)  # PlaylistTrack


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

    # ########  AUTOMATIC DATA SEEDING  ########
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(func.count()).select_from(Album))
        row_count = result.scalar()
        if row_count == 0:
            log.warn("⚠️  Album (albums) table is empty!!!  Seeding all ERP (Chinook) mock data...")
            log.warn("⚠️️  IMPORTANT!  ⛔  PLEASE WAIT UNTIL DATA LOADING COMPLETES IN A FEW MINUTES  ⛔")
            # TODO: Add maintenance mode which disables access to all endpoints of the API. Enter maintenance mode here.
            # Loading in depdendency order (children first). See table dependency comments at the end of this file.
            await seed_erp_data(session)
            # TODO: Exit maintenance mode here, restoring access to all API endpoints.
        else:
            log.info(f"✅ Album (albums) table already has {row_count} rows. Skipping seed.")


# ########  ERP (Chinook) DATA SEEDING  ########
#
# NOTE: The loading process adds a (UTC) timezone awareness to all date/time columns in any of the Chinook CSV files.
# To follow best-practices, our entire stack is timezone aware and to simplify greatly the handling of timezone-naive
# data, the best solution is to make that data timezone aware (in the UTC timezone or whatever zone is most appropriate)
# even before seeding/loading through models or schemas. We have a nice built-in mechanism to do this using the
# "datetime_fields" optional argument below. To use it you must specify the column names of any date/time column in
# the CSV file which does not include timezone information. For Chinook, there are only three:
#    Employee.csv:  Birthdate, HireDate
#    Invoice.csv:  InvoiceDate
#
async def seed_erp_data(session: AsyncSession):
    await load_csv(
            session,
            model_name='genre',
            file_path="data/chinook/Genre.csv",
            pydantic_create_schema=GenreCreate,
            sqlalchemy_model=Genre,
            datetime_fields=[],
        )
    await load_csv(
            session,
            model_name='media_type',
            file_path="data/chinook/MediaType.csv",
            pydantic_create_schema=MediaTypeCreate,
            sqlalchemy_model=MediaType,
            datetime_fields=[],
        )
    await load_csv(
            session,
            model_name='artist',
            file_path="data/chinook/Artist.csv",
            pydantic_create_schema=ArtistCreate,
            sqlalchemy_model=Artist,
            datetime_fields=[],
        )
    await load_csv(
            session,
            model_name='album',
            file_path="data/chinook/Album.csv",
            pydantic_create_schema=AlbumCreate,
            sqlalchemy_model=Album,
            datetime_fields=[],
        )
    await load_csv(
            session,
            model_name='track',
            file_path="data/chinook/Track.csv",
            pydantic_create_schema=TrackCreate,
            sqlalchemy_model=Track,
            datetime_fields=[],
        )
    await load_csv(
            session,
            model_name='employee',
            file_path="data/chinook/Employee.csv",
            pydantic_create_schema=EmployeeCreate,
            sqlalchemy_model=Employee,
            datetime_fields=["Birthdate", "HireDate"],  # 2 date/time columns to add UTC timezone to in Employee.csv
        )
    await load_csv(
            session,
            model_name='customer',
            file_path="data/chinook/Customer.csv",
            pydantic_create_schema=CustomerCreate,
            sqlalchemy_model=Customer,
            datetime_fields=[],
        )
    await load_csv(
            session,
            model_name='invoice',
            file_path="data/chinook/Invoice.csv",
            pydantic_create_schema=InvoiceCreate,
            sqlalchemy_model=Invoice,
            datetime_fields=["InvoiceDate"],  # 1 date/time column to add UTC timezone to in Invoice.csv
        )
    await load_csv(
            session,
            model_name='invoice_line',
            file_path="data/chinook/InvoiceLine.csv",
            pydantic_create_schema=InvoiceLineCreate,
            sqlalchemy_model=InvoiceLine,
            datetime_fields=[],
        )
    await load_csv(
            session,
            model_name='playlist',
            file_path="data/chinook/Playlist.csv",
            pydantic_create_schema=PlaylistCreate,
            sqlalchemy_model=Playlist,
            datetime_fields=[],
        )
    await load_csv(
            session,
            model_name='playlist_track',
            file_path="data/chinook/PlaylistTrack.csv",
            pydantic_create_schema=PlaylistTrackCreate,
            sqlalchemy_model=PlaylistTrack,
            datetime_fields=[],
        )


# Based on relationships in the well-known Chinook DB schema, we must load the CSV mock data in the
# correct child-parent order of dependency. Without loading in this order, some table rows will start loading which
# have foreign keys in them which point to related rows which do not exist yet. Our DB has foreign key constraints
# in place at the time of loading so that would result in errors. If we load in dependency order, you don't have
# this problem. The seeding order we have configured above is based on the following:
#
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

