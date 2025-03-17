

import os
from dotenv import load_dotenv

load_dotenv()

GITLAB_API_URL = os.getenv("GITLAB_API_URL", "https://gitlab.boon.com.au/api/v4")
GITLAB_PRIVATE_TOKEN = os.getenv("GITLAB_PRIVATE_TOKEN", "personalY5x4w3Cme8yqUjMoxmyi")

DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///gitlab_data.db")

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_DIR = "logs"
