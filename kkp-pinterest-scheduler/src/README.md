# Pinterest Scheduler

A Python application that schedules Pinterest pins using the Pinterest API v5, with integration for Raspberry Pi image storage.

## Features

- Process pins from CSV files
- Automatically transfer images to Raspberry Pi
- Schedule pins at specific times (6am, 7am, 12pm, 6pm, and 7pm)
- SQLite database for pin management
- Logging system for tracking operations

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
PINTEREST_ACCESS_TOKEN=your_pinterest_access_token
RASPBERRY_PI_HOST=your_raspberry_pi_ip
RASPBERRY_PI_USER=your_raspberry_pi_username
RASPBERRY_PI_PASSWORD=your_raspberry_pi_password
RASPBERRY_PI_IMAGE_DIR=/path/to/images/on/raspberry/pi

4. Prepare your CSV file with the following columns:
- title
- description
- board
- image_path

## Usage

Run the scheduler:
```bash
python scheduler.py
```

The scheduler will:
- Run at scheduled times (6am, 7am, 12pm, 6pm, and 7pm)
- Process the oldest pending pin at each scheduled time
- Transfer images to the Raspberry Pi
- Create pins on Pinterest
- Log all operations

## CSV Format Example

```csv
title,description,board,image_path
My Pin Title,A great description,my-board/section,/path/to/local/image.jpg
```