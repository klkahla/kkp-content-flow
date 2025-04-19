# Pinterest Scheduler

A Python application that schedules Pinterest pins using the Pinterest API v5, with integration for Raspberry Pi image storage and PostgreSQL database.

## Features

- Process pins from CSV files
- Automatically transfer images to Raspberry Pi
- Schedule pins at specific times (6am, 7am, 12pm, 6pm, and 7pm)
- PostgreSQL database for pin management
- Logging system for tracking operations

## Prerequisites

- Python 3.8 or higher
- Raspberry Pi with PostgreSQL installed
- Pinterest API access token

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure the `.env` file with your credentials:
```bash
# Pinterest API settings
PINTEREST_ACCESS_TOKEN=your_pinterest_access_token

# Raspberry Pi settings
RASPBERRY_PI_HOST=your_raspberry_pi_ip
RASPBERRY_PI_USER=your_raspberry_pi_username
RASPBERRY_PI_PASSWORD=your_raspberry_pi_password
RASPBERRY_PI_IMAGE_DIR=/path/to/images/on/raspberry/pi

# Database settings
DB_HOST=your_raspberry_pi_ip  # Defaults to RASPBERRY_PI_HOST if not specified
DB_PORT=5432
DB_NAME=pinterest_db
DB_USER=your_raspberry_pi_username  # Defaults to RASPBERRY_PI_USER if not specified
DB_PASSWORD=your_raspberry_pi_password  # Defaults to RASPBERRY_PI_PASSWORD if not specified
```

4. Set up PostgreSQL on Raspberry Pi:
```bash
# Install PostgreSQL
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib

# Create database and user
sudo -u postgres psql
CREATE DATABASE pinterest_db;
CREATE USER your_raspberry_pi_user WITH PASSWORD 'your_raspberry_pi_password';

-- Create the user with login privilege
CREATE USER your_raspberry_pi_user WITH PASSWORD 'your_raspberry_pi_password' LOGIN;

-- Create the database with the user as owner
CREATE DATABASE pinterest_db OWNER your_raspberry_pi_user;

-- Connect to the pinterest_db
\c pinterest_db

-- Grant all privileges on the database
GRANT ALL PRIVILEGES ON DATABASE pinterest_db TO your_raspberry_pi_user;

-- Grant schema privileges
GRANT ALL ON SCHEMA public TO your_raspberry_pi_user;
ALTER SCHEMA public OWNER TO your_raspberry_pi_user;

-- Grant table privileges
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO your_raspberry_pi_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO your_raspberry_pi_user;

-- Set default privileges for future objects
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO your_raspberry_pi_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO your_raspberry_pi_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON FUNCTIONS TO your_raspberry_pi_user;
\q

# Configure PostgreSQL for remote connections
# Edit /etc/postgresql/[version]/main/postgresql.conf:
# listen_addresses = '*'

# Edit /etc/postgresql/[version]/main/pg_hba.conf:
# host    all             all             0.0.0.0/0               md5

# Restart PostgreSQL
sudo systemctl restart postgresql

# Allow PostgreSQL port in firewall
sudo apt-get install ufw
sudo ufw allow 5432/tcp
```

## CSV Format

Prepare your CSV file with the following columns:
```csv
file_name,title,description,board_id,link
My Pin Title,A great description,couples,/path/to/local/image.jpg
```

Available board options:
- couples
- weddings
- wedding_inspo

## Usage

1. Process a CSV file:
```bash
python csv_processor.py path/to/your/file.csv
```

2. Run the scheduler:
```bash
python scheduler.py
```

The scheduler will:
- Run at scheduled times (6am, 7am, 12pm, 6pm, and 7pm)
- Process the oldest pending pin at each scheduled time
- Transfer images to the Raspberry Pi
- Create pins on Pinterest
- Log all operations

## Checking Database

To check the database contents on the Raspberry Pi:
```bash
psql -U your_raspberry_pi_user -d pinterest_db -h localhost
```

Useful PostgreSQL commands:
```sql
-- List all tables
\dt

-- View all pins
SELECT * FROM pins;

-- Count total pins
SELECT COUNT(*) FROM pins;

-- View most recent pins
SELECT title, created_at FROM pins ORDER BY created_at DESC LIMIT 5;
```

## Project Structure

```
.
├── config/
│   └── settings.py         # Configuration settings
├── models/
│   └── pin.py             # Database models
├── services/
│   ├── csv_handler.py     # CSV processing
│   ├── file_transfer.py   # Raspberry Pi file transfer
│   ├── pinterest.py       # Pinterest API integration
│   └── email_service.py   # Email notifications
├── utils/
│   └── logger.py          # Logging configuration
├── csv_processor.py       # CSV processing script
├── scheduler.py           # Main scheduler
└── requirements.txt       # Project dependencies
```

## Logging

Logs are stored in the `logs` directory with the format:
```
logs/pinterest_scheduler_YYYYMMDD.log
```

## Error Handling

- Failed pin creations are logged
- Email notifications are sent for failures (if configured)
- Database transactions are rolled back on errors
- File transfer errors are logged and reported