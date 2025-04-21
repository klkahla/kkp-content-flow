import pandas as pd
import os
from models.pin import Pin
from utils.logger import logger

class CSVHandler:
    def __init__(self):
        return

    def get_board_id(self, board_name):
        """
        Get the Pinterest board ID based on the board name
        """
        board_name = board_name.lower()
        if board_name == 'couples':
            return os.getenv('PINTEREST_BOARD_ID_COUPLES')
        elif board_name == 'weddings':
            return os.getenv('PINTEREST_BOARD_ID_WEDDINGS')
        elif board_name == 'wedding_inspo':
            return os.getenv('PINTEREST_BOARD_ID_WEDDING_INSPIRATION')
        else:
            logger.error(f"Board ID not found for board: {board_name}")
            return None

    def process_csv(self, csv_path):
        """
        Process the CSV file and transfer images to Raspberry Pi
        """
        try:
            df = pd.read_csv(csv_path)
            
            for _, row in df.iterrows():
                # Get board ID
                board_id = self.get_board_id(row['board_id'])
                if not board_id:
                    continue

                # Transfer image to AWS S3
                s3_path = ""

                # Create database record in DynamoDB
                print(f"Creating database record for pin")
                pin = Pin(
                    link=row['link'],
                    title=row['title'],
                    description=row['description'],
                    image_path=s3_path,
                    board_id=board_id
                )
                
                # TODO: Add pin to DynamoDB

                print(f"(Done adding pin)")
            
            
            logger.info("Successfully processed all pins from CSV")
        except Exception as e:
            logger.error(f"Error processing CSV: {str(e)}")
            raise
        