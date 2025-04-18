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
DB_HOST = os.getenv('DB_HOST', RASPBERRY_PI_HOST)  # Default to Raspberry Pi host if not specified
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'pinterest_db')
DB_USER = os.getenv('DB_USER', RASPBERRY_PI_USER)  # Default to Raspberry Pi user if not specified
DB_PASSWORD = os.getenv('DB_PASSWORD', RASPBERRY_PI_PASSWORD)  # Default to Raspberry Pi password if not specified

DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'