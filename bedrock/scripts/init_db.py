#! /usr/bin/env python

from magma.core.logger import log
import asyncio
from magma.core.database import async_engine, Base


async def init_db():
    async with async_engine.begin() as conn:
        log.info(f"🚧🚧  Running: DB CREATE_ALL (via 📝 init_db script 📝 )  🚧🚧")
        await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    asyncio.run(init_db())

