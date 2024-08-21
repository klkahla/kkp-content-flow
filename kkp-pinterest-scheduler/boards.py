import sys
import requests
import argparse
from os.path import abspath, dirname, join
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add the directory containing access_token.py to the Python path
module_path = abspath(join(dirname(__file__), "..", "kkp-pinterest-scheduler/pinterest-api-quickstart", "src"))
if module_path not in sys.path:
    sys.path.append(module_path)

from api_config import ApiConfig
from board import Board
from user import User

class Board:
    def __init__(self, id, name, description, privacy):
        self.id = id
        self.name = name
        self.description = description
        self.privacy = privacy


def get_user_boards(args, access_token):
    args.page_size = 25
    args.include_empty = False
    args.privacy = "PUBLIC"

     # get configuration from defaults and/or the environment
    api_config = ApiConfig(verbosity=args.log_level)

    # get information about all of the boards in the user's profile
    user = User(api_config, access_token)
    query_parameters = {"page_size": args.page_size}
    if args.include_empty:
        query_parameters["include_empty"] = args.include_empty

    boards = []
    board_iterator = user.get_boards(query_parameters)
    for board in board_iterator:
        print(board)
        boards.append(Board(
            id=board["id"],
            name=board["name"],
            description=board["description"],
            privacy=board["privacy"]
        ))
    user.print_multiple(args.page_size, "board", Board, board_iterator)
    return boards


def get_last_pin(board_id, access_token):
    print(access_token.access_token)
    url = f"https://api.pinterest.com/v5/boards/{board_id}/pins?board_id={board_id}"
    headers = {
        "Authorization": f"Bearer {access_token.access_token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    params = {
        "page_size": 1,  # Get only the most recent pin
        "sort": "newest"  # Sort pins by newest first
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Raise an error for bad status codes
        pins = response.json().get('items', [])
        
        if pins:
            print(f"Last created pin: {pins[0]}")
            return pins[0]
        else:
            print("No pins found on the board.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch pins: {e}")
        return None