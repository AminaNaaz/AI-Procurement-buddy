# utils/logger.py

import logging
import os

# Ensure logs directory exists
os.makedirs("logs", exist_ok=True)

# Configure logger
logging.basicConfig(
    filename="logs/app.log",             # Log file path
    filemode="a",                        # Append mode
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO                   # Use DEBUG for more verbose logging
)

# Create logger instance
logger = logging.getLogger("app_logger")
logger.setLevel(logging.INFO)
