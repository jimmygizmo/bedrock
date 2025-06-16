import os
import logging
from enum import Enum
from dataclasses import dataclass

log = logging.getLogger(__name__)


class StackEnv(str, Enum):
    DEVELOPMENT = "development"
    TESTING = "testing"
    PRODUCTION = "production"


def get_required_env(key: str) -> str:
    value = os.getenv(key)
    if not value:
        raise EnvironmentError(f"🟥 Missing required environment variable: {key}")
    return value


def get_bool_env(key: str, default: bool = False) -> bool:
    val = os.getenv(key)
    if val is None:
        return default
    return val.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    stack_env: StackEnv
    debug_mode: bool
    feature_flag_xyz: bool  # Example additional flag

    @classmethod
    def load(cls) -> "Settings":
        raw_stack_env = get_required_env("STACK_ENV")
        try:
            stack_env = StackEnv(raw_stack_env.lower())
        except ValueError:
            raise ValueError(
                f"🟥 Invalid STACK_ENV: {raw_stack_env!r}. Must be one of: "
                f"{', '.join(e.value for e in StackEnv)}"
            )

        debug_mode = get_bool_env("DEBUG", default=False)
        feature_flag_xyz = get_bool_env("FEATURE_XYZ", default=False)

        log.info(f"✅ STACK_ENV: {stack_env}")
        log.info(f"🐞 DEBUG_MODE: {debug_mode}")
        log.info(f"🧪 FEATURE_XYZ: {feature_flag_xyz}")

        return cls(
            stack_env=stack_env,
            debug_mode=debug_mode,
            feature_flag_xyz=feature_flag_xyz,
        )


# Load settings once, accessible app-wide
settings = Settings.load()


# EXAMPLE USAGE:
# from settings import settings
#
# if settings.stack_env == StackEnv.PRODUCTION and settings.debug_mode:
#     log.warning("🟠 DEBUG MODE ENABLED IN PRODUCTION!")
#
# if settings.feature_flag_xyz:
#     log.info("🧪 Running with experimental FEATURE_XYZ")

