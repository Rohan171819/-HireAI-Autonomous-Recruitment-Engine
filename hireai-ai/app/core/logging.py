import sentry_sdk
from loguru import logger
import sys
from app.core.config import settings

# Sentry Initialization
sentry_sdk.init(
    dsn=settings.SENTRY_DSN, 
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)

# Structured Logging Configuration
logger.remove()
logger.add(
    sys.stderr, 
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="INFO"
)
logger.add("logs/app.log", rotation="10 MB", retention="10 days", compression="zip")

def get_logger():
    return logger
