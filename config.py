import os
from dotenv import load_dotenv

load_dotenv("config.env")  # or just load_dotenv() if you rename to .env

API_KEY = os.getenv("WATSON_API_KEY")

SERVICE_URL = os.getenv("WATSON_SERVICE_URL")
VERSION = "2023-03-31"
