#! /usr/bin/env python

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import magma.core.config as cfg
from magma.core.logger import log
from magma.routers import users
from magma.core.database import async_engine, Base

# FOR SEEDING:
from sqlalchemy import select, func
from magma.models.erp.album import Album
from magma.models.erp.artist import Artist
from magma.models.erp.customer import Customer
from magma.models.erp.employee import Employee
from magma.models.erp.genre import Genre
from magma.models.erp.invoice import Invoice
from magma.models.erp.invoice_line import InvoiceLine
from magma.models.erp.media_type import MediaType
from magma.models.erp.playlist import Playlist
from magma.models.erp.playlist_track import PlaylistTrack
from magma.models.erp.track import Track

from magma.seed.seed import load_albums, load_artists, load_tracks
# from magma.seed.seed import load_albums, load_artists, load_customers, load_employees, load_genres, load_invoices
# from magma.seed.seed import load_invoice_lines, load_media_types, load_playlists, load_playlist_tracks, load_tracks
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession


# ########  ENTRYPOINT: Bedrock Platform - FastAPI Application:  magma  ########


log.info("🔥🔥🔥  BEDROCK MAGMA STARTING  🔥🔥🔥")

app = None  # Ensures global scope visibility for guvicorn

if cfg.stack_env == 'DEVELOPMENT':
    app = FastAPI()
    log.info(f"⚠️  Swagger/OpenAPI/ReDoc enabled.  Danger!!!  ⛔  DEVELOPMENT  ⛔  - "
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
            log.warn("⚠️  Album (albums) table is empty!!!  Seeding all ERP data...")
            log.warn("⚠️️  IMPORTANT!  ⛔  PLEASE WAIT UNTIL DATA LOADING COMPLETES IN A FEW MINUTES  ⛔")
            # IMPORTANT: For foreign key integrity, you must load in depdendency order - children first
            await load_artists(session, file_path="data/chinook/Artist.csv")
            await load_albums(session, file_path="data/chinook/Album.csv")
            # await load_media_types(session, file_path="data/chinook/MediaType.csv")
            # await load_genres(session, file_path="data/chinook/Genre.csv")
            await load_tracks(session, file_path="data/chinook/Track.csv")
            #
            # await load_customers(session, file_path="data/chinook/Customer.csv")
            # await load_employees(session, file_path="data/chinook/Employee.csv")
            # await load_invoices(session, file_path="data/chinook/Invoice.csv")
            # await load_invoice_lines(session, file_path="data/chinook/InvoiceLine.csv")
            # await load_playlists(session, file_path="data/chinook/Playlist.csv")
            # await load_playlist_tracks(session, file_path="data/chinook/PlaylistTrack.csv")
        else:
            log.info(f"Album (albums) table already has {row_count} rows. Skipping seed.")

