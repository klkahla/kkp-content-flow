#!/usr/bin/env python3

import sys
import argparse
from os.path import abspath, dirname, join
from dotenv import load_dotenv
import csv

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
from boards import Board, get_user_boards

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

def read_csv_file(csv_file_path):
    pins = []
    with open(csv_file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            pins.append(row)
    return pins

def main(argv=[]):
    parser = argparse.ArgumentParser(description="Select a Board")
    common_arguments(parser)
    args = parser.parse_args(argv)

    # get configuration from defaults and/or the environment
    api_config = ApiConfig(verbosity=args.log_level)

    # Note: It's possible to use the same API configuration with
    # multiple access tokens, so these objects are kept separate.
    access_token = AccessToken(api_config, name=args.access_token)
    access_token.fetch(scopes=[Scope.READ_USERS, Scope.READ_BOARDS])

    # get information about all of the boards in the user's profile
    user = User(api_config, access_token)
    boards = get_user_boards(args, access_token)
    selected_board = select_board(boards)
    print(f"Selected board: {selected_board.name} (ID: {selected_board.id})")

    # Prompt for CSV file
    csv_file_path = prompt_for_csv_file()
    pins = read_csv_file(csv_file_path)
    print(f"Loaded {len(pins)} pins from {csv_file_path}")

if __name__ == "__main__":
    main(sys.argv[1:])