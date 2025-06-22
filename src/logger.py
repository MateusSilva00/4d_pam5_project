from loguru import logger

logger.add(
    "logs/app.log",
    rotation="1 MB",
    retention="10 days",
    level="DEBUG",
    format="{time} {level} {message}",
)

logger.add(
    "logs/error.log",
    rotation="1 MB",
    retention="10 days",
    level="ERROR",
    format="{time} {level} {message}",
)
