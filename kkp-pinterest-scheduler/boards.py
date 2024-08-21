import subprocess
import json
import sys
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