import dotenv
import os
from magma.core.logger import log


# ########    CONFIGURATION:  SETTINGS & ENVIRONMENT    ########

# ----  BASIC SETTINGS

# When True and only for log.debug() calls, show log messages that contain sensitive information like passwords.
DEBUG_LOG_SECRETS_OK = False  # Should normally be False


# ----  CONSTANTS

DBNAME: str = 'bedrockdb'
DBHOST: str = 'bedrock-postgres'


# ----  ENVIRONMENT LOADING

# NOTE: ENV FASTAPI_LOG_LEVEL is processed inside magma.core.logger so that logging is available early.

dotenv.load_dotenv(dotenv.find_dotenv())

log.info(f"☑️ CWD via os.getcwd(): {os.getcwd()}")  # (Debug .env loading.)

stack_env: str = os.getenv("STACK_ENV", "🟥 ERROR: MISSING ENV VAR:  STACK_ENV")
log.info(f"✅ STACK_ENV: {stack_env}")  # Controls SAFETY FACTORS FOR PRODUCTION and more.

postgres_user: str = os.getenv("POSTGRES_USER", "🟥 ERROR: MISSING ENV VAR:  POSTGRES_USER")
if DEBUG_LOG_SECRETS_OK:
    log.debug(f"✅ ⚠️ POSTGRES_USER: {postgres_user}  ❗ INSECURE ❗")

postgres_password: str = os.getenv("POSTGRES_PASSWORD", "🟥 ERROR: MISSING ENV VAR:  POSTGRES_PASSWORD")
if DEBUG_LOG_SECRETS_OK:
    log.debug(f"✅ ⚠️ POSTGRES_PASSWORD: {postgres_password}  ❗ INSECURE ❗")


# ----  COMPOSITE CONFIG VALUES

DATABASE_URL: str = f"postgresql+asyncpg://{postgres_user}:{postgres_password}@{DBHOST}/{DBNAME}"

if DEBUG_LOG_SECRETS_OK:
    log.debug(f"✅ ⚠️ Composed DATABASE_URL: {DATABASE_URL}  ❗ INSECURE ❗")


# ----  SPECIAL SETTINGS

# -- DB CREATION/INITIALIZATION & SCHEMA UPDATES

# NOTE: None of the 3 methods below are appropriate for commercial applications or even medium-sized simple apps.
#   These are for special use cases, including as a temporary option, prior to the integration of Alembic.
#   Of all 3, option # 3 below is the best for simply creating and updating the DB of very simple apps.

# 1.  CREATE_ON_EACH_CALL
# For experiments, troubleshooting and special use cases. Warning this is extreme and triggers on every DB call.
# This should not hurt anything in most small applications but is not what you want for normal use.
CREATE_ON_EACH_CALL = False
if CREATE_ON_EACH_CALL:
    log.info(f"✅ ⚠️ CREATE_ON_EACH_CALL: {str(CREATE_ON_EACH_CALL)}   ❗ EXCESSIVE ❗)")

# 2.  CREATE_ON_STARTUP
# For special use cases or as an interim solution; pre-Alembic. Warning this is crude and triggers on every DB startup.
# This should not hurt anything in most applications but is not at all optimal.
# This could work OK for small, simple apps, but not for commercial/larger apps.
# DB creation/initialization and data seeding as well as migrations forward and backwards will be handled by Alembic.
# Alembic is coming soon, but until it is added to Bedrock, this is a good option for creating/updating the DB schema:
CREATE_ON_STARTUP = True
if CREATE_ON_STARTUP:
    log.info(f"✅ ⚠️ CREATE_ON_STARTUP: {str(CREATE_ON_STARTUP)}    (IMPORTANT: Temporary solution. Not optimal.)")

# 3.  /scripts/init_db.py
# Prior to Alembic coming, there is another option for DB creation and it is perhaps preferable to the above 2 methods.
# Simply run the script:  /scripts/init_db.py

