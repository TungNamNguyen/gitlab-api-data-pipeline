"""
Module cấu hình cho ứng dụng trích xuất dữ liệu GitLab API.

Module này tải các biến môi trường và cung cấp cài đặt cấu hình
cho ứng dụng.
"""

import os
from dotenv import load_dotenv

# Tải biến môi trường từ file .env
load_dotenv()

# Cấu hình GitLab API
GITLAB_API_URL = os.getenv("GITLAB_API_URL", "https://gitlab.boon.com.au/api/v4")
GITLAB_PRIVATE_TOKEN = os.getenv("GITLAB_PRIVATE_TOKEN", "personalY5x4w3Cme8yqUjMoxmyi")

# Cấu hình cơ sở dữ liệu
DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///gitlab_data.db")

# Cấu hình logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_DIR = "logs"
