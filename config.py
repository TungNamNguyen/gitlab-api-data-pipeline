"""
Configuration module for the GitLab API data extraction application.

Instead of retrieving the token from an environment variable, 
the application prompts the user to enter the token at runtime (without hardcoding it).
"""


import getpass

GITLAB_API_URL = "https://gitlab.boon.com.au/api/v4"

token = getpass.getpass("Private Token: ")
GITLAB_PRIVATE_TOKEN = token

DATABASE_URI = "sqlite:///gitlab_data.db"

LOG_LEVEL = "INFO"
LOG_DIR = "logs"