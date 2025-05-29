import magma.core.config as cfg
from magma.core.logger import log
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base


# ########    DATABASE INITIALIZATION    ########

async_engine = create_async_engine(cfg.DATABASE_URL)

log.debug(f"🔵  Async DB session initialized  🔵")

Base = declarative_base()  # Pydantic Declarative Base - Reference DB schema used for database creation/changes

