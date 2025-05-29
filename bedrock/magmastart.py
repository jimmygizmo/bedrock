#! /usr/bin/env python

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import magma.core.config as cfg
from magma.core.logger import log
from magma.routers import users
from magma.core.database import async_engine, Base


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
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)


# ########  ROUTERS  ########

app.include_router(users.router)  # Users


# ########  ROOT API HANDLERS  ########

@app.get("/")
async def root():
    return {"message": "This is the root/default app in Bedrock Magma"}


# ########  EVENT HANDLERS  ########
# (Deprecated. Useful in special cases.)

@app.on_event("startup")
async def on_startup():
    log.debug(f"🚧🚧  Running: DB CREATE_ALL (via 🚀 startup 🚀 event)  🚧🚧")
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

