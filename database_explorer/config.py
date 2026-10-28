"""Application settings loaded from environment variables and .env."""

import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
DEFAULT_ROW_LIMIT = 100
MAX_ROW_LIMIT = 500
STATEMENT_TIMEOUT_MS = 3_000
