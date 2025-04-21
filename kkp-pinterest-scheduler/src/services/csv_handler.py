import pandas as pd
import os
from models.pin import Session, Pin
from services.file_transfer import FileTransferService
from utils.logger import logger

class CSVHandler:
    def __init__(self):
        self.file_transfer = FileTransferService()
        self.session = Session()

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

                # Transfer image to Raspberry Pi
                local_image_path = row['file_name']
                # Get just the filename from the full path
                local_image_name = os.path.basename(local_image_path)
                print(f"Transferring local image {local_image_name} to Raspberry Pi")
                remote_path = self.file_transfer.transfer_file(
                    local_image_path, 
                    local_image_name
                )

                # Create database record
                print(f"Creating database record for pin")
                pin = Pin(
                    link=row['link'],
                    title=row['title'],
                    description=row['description'],
                    image_path=remote_path,
                    board_id=board_id
                )
                self.session.add(pin)

                print(f"(Done adding pin)")
            
            self.session.commit()
            logger.info("Successfully processed all pins from CSV")
        except Exception as e:
            self.session.rollback()
            logger.error(f"Error processing CSV: {str(e)}")
            raise
        finally:
            self.session.close()