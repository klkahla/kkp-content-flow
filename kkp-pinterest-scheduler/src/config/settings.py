import os
from dotenv import load_dotenv

load_dotenv()

# Pinterest API settings
PINTEREST_ACCESS_TOKEN = os.getenv('PINTEREST_ACCESS_TOKEN')

# Raspberry Pi settings
RASPBERRY_PI_HOST = os.getenv('RASPBERRY_PI_HOST')
RASPBERRY_PI_USER = os.getenv('RASPBERRY_PI_USER')
RASPBERRY_PI_PASSWORD = os.getenv('RASPBERRY_PI_PASSWORD')
RASPBERRY_PI_IMAGE_DIR = os.getenv('RASPBERRY_PI_IMAGE_DIR')

# Database settings
DATABASE_URL = 'sqlite:///pinterest.db'