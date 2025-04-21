from services.csv_handler import CSVHandler
from utils.logger import logger
from dotenv import load_dotenv
import sys

load_dotenv()

class CSVProcessor:
    def __init__(self):
        self.csv_handler = CSVHandler()

    def process_csv(self, csv_path):
        """
        Process the CSV file and transfer images to Raspberry Pi
        """
        try:
            # Process the CSV file
            self.csv_handler.process_csv(csv_path)

            logger.info("CSV file processed successfully")
        except Exception as e:
            logger.error(f"Error processing CSV file: {str(e)}")
            raise

def main():
    processor = CSVProcessor()
    
    # Get file name from command line
    if len(sys.argv) != 2:
        logger.error("Please provide the CSV file path as an argument")
        sys.exit(1)

    csv_file = sys.argv[1]
    logger.info(f"Processing CSV file: {csv_file}")

    # Process the CSV file
    processor.process_csv(csv_file)


if __name__ == "__main__":
    main()