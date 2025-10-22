import os

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')

API_URL = os.getenv('API_URL')
API_HEADERS = {}
WEBHOOK_URL = os.getenv("WEBHOOK_URL")