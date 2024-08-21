#!/usr/bin/env python3

import sys
import argparse
from os.path import abspath, dirname, join
from dotenv import load_dotenv
import csv
from datetime import datetime, timedelta
import pytz

# Load environment variables from .env file
load_dotenv()

# Add the directory containing access_token.py to the Python path
module_path = abspath(join(dirname(__file__), "..", "kkp-pinterest-scheduler/pinterest-api-quickstart", "src"))
if module_path not in sys.path:
    sys.path.append(module_path)

from access_token import AccessToken
from api_config import ApiConfig
from arguments import common_arguments
from oauth_scope import Scope
from user import User
from boards import Board, get_user_boards, get_last_pin

def select_board(boards):
    print("Select a board:")
    for idx, board in enumerate(boards):
        print(f"{idx + 1}. {board.name} (ID: {board.id})")
    selection = int(input("Enter the number of the board: ")) - 1
    if selection < 0 or selection >= len(boards):
        print("Invalid selection")
        sys.exit(1)
    return boards[selection]

def prompt_for_csv_file():
    csv_file_path = input("Enter the path to the CSV file of pins to schedule: ")
    return csv_file_path

def prompt_for_pin_description():
    description = input("Enter the description for all pins: ")
    return description

def prompt_for_pin_link():
    pin_link = input("Enter the link for all pins: ")
    return pin_link

def read_csv_file(csv_file_path):
    pins = []
    with open(csv_file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            pins.append(row)
    return pins

TIME_SLOTS = [6, 7, 12, 18, 19]  # Time slots in 24-hour format (Mountain Time)

def get_next_available_time(last_pin_time):
    now_utc = datetime.now(pytz.utc)
    mountain_tz = pytz.timezone('US/Mountain')
    now_mt = now_utc.astimezone(mountain_tz)

    if last_pin_time.date() < now_mt.date():
        for hour in TIME_SLOTS:
            next_time_mt = now_mt.replace(hour=hour, minute=0, second=0, microsecond=0)
            next_time_utc = next_time_mt.astimezone(pytz.utc)
            if next_time_utc > now_utc:
                return next_time_utc
        # If no time slot is available today, schedule for the first slot tomorrow
        next_time_mt = now_mt.replace(hour=6, minute=0, second=0, microsecond=0) + timedelta(days=1)
        return next_time_mt.astimezone(pytz.utc)
    
    for hour in TIME_SLOTS:
        next_time_mt = last_pin_time.astimezone(mountain_tz).replace(hour=hour, minute=0, second=0, microsecond=0)
        next_time_utc = next_time_mt.astimezone(pytz.utc)
        if next_time_utc > last_pin_time:
            return next_time_utc
    
    next_time_mt = last_pin_time.astimezone(mountain_tz) + timedelta(days=1, hours=6 - last_pin_time.hour)
    return next_time_mt.astimezone(pytz.utc)

def generate_pin_schedule(last_pin, pins, description, pin_link):
    # The next pin should fall after the last pin on the board
    # If that last pin is later than today, move next pin to today
    # Pins are created at 6am, 7am, 12pm, 6pm and 7pm. One pin per time slot per day
    # Choose the next available time and then loop through remaining pins moving to the next time/day as needed
    last_pin_time = datetime.strptime(last_pin['created_at'], '%Y-%m-%dT%H:%M:%S').replace(tzinfo=pytz.utc)
    scheduled_pins = []

    for pin in pins:
        next_time = get_next_available_time(last_pin_time)
        pin['title'] = pin['title']
        pin['description'] = description
        pin['link'] = pin_link
        pin['scheduled_time'] = next_time.strftime('%Y-%m-%dT%H:%M:%S')
        scheduled_pins.append(pin)
        last_pin_time = next_time

    return scheduled_pins


def main(argv=[]):
    parser = argparse.ArgumentParser(description="Select a Board")
    common_arguments(parser)
    args = parser.parse_args(argv)

    # get configuration from defaults and/or the environment
    api_config = ApiConfig(verbosity=args.log_level)

    # Note: It's possible to use the same API configuration with
    # multiple access tokens, so these objects are kept separate.
    access_token = AccessToken(api_config, name=args.access_token)
    access_token.fetch(scopes=[Scope.READ_USERS, Scope.READ_BOARDS, Scope.WRITE_PINS, Scope.READ_PINS])

    # get information about all of the boards in the user's profile
    user = User(api_config, access_token)
    boards = get_user_boards(args, access_token)
    selected_board = select_board(boards)
    print(f"Selected board: {selected_board.name} (ID: {selected_board.id})")

    last_pin = get_last_pin(selected_board.id, access_token)
    print(f"Last pin: {last_pin}")

    csv_file_path = prompt_for_csv_file()
    pins = read_csv_file(csv_file_path)

    description = prompt_for_pin_description()
    pin_link = prompt_for_pin_link()

    # Generate pin schedule for pins
    scheduled_pins = generate_pin_schedule(last_pin, pins, description, pin_link)
    for pin in scheduled_pins:
        print(f"Scheduled pin: {pin['file_name']} at {pin['scheduled_time']}")


if __name__ == "__main__":
    main(sys.argv[1:])