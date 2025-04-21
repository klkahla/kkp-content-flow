import os
from dotenv import load_dotenv

load_dotenv()

# Pinterest API settings
PINTEREST_ACCESS_TOKEN = os.getenv('PINTEREST_ACCESS_TOKEN')
