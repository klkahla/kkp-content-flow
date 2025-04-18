import pandas as pd
import os
from src.models.pin import Session, Pin
from src.services.file_transfer import FileTransferService

class CSVHandler:
    def __init__(self):
        self.file_transfer = FileTransferService()
        self.session = Session()

    def process_csv(self, csv_path):
        """
        Process the CSV file and transfer images to Raspberry Pi
        """
        try:
            df = pd.read_csv(csv_path)
            
            for _, row in df.iterrows():
                # Transfer image to Raspberry Pi
                local_image_path = row['image_path']
                remote_filename = os.path.basename(local_image_path)
                remote_path = self.file_transfer.transfer_file(
                    local_image_path, 
                    remote_filename
                )

                # Create database record
                pin = Pin(
                    title=row['title'],
                    description=row['description'],
                    image_path=remote_path,
                    board=row['board']
                )
                self.session.add(pin)
            
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            print(f"Error processing CSV: {str(e)}")
            raise
        finally:
            self.session.close()