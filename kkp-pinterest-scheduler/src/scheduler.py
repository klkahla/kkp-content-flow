import schedule
import time
from datetime import datetime
from src.models.pin import Session, Pin
from src.services.pinterest import PinterestService
from src.services.csv_handler import CSVHandler
from src.utils.logger import logger
from dotenv import load_dotenv

load_dotenv()

class PinterestScheduler:
    def __init__(self):
        self.pinterest_service = PinterestService()
        self.session = Session()

    def process_next_pin(self):
        """
        Process the oldest pending pin
        """
        try:
            # Get the oldest pending pin
            pin = self.session.query(Pin)\
                .filter(Pin.status == 'pending')\
                .order_by(Pin.created_at.asc())\
                .first()

            if not pin:
                logger.info("No pending pins found")
                return

            # Create pin on Pinterest
            self.pinterest_service.create_pin(pin)

            # Update pin status
            pin.status = 'posted'
            pin.posted_at = datetime.utcnow()
            self.session.commit()
            logger.info(f"Successfully posted pin: {pin.title}")

        except Exception as e:
            logger.error(f"Error processing pin: {str(e)}")
            if pin:
                pin.status = 'failed'
                self.session.commit()
        finally:
            self.session.close()

def main():
    scheduler = PinterestScheduler()
    
    # Schedule jobs
    schedule.every().day.at("06:00").do(scheduler.process_next_pin)
    schedule.every().day.at("07:00").do(scheduler.process_next_pin)
    schedule.every().day.at("12:00").do(scheduler.process_next_pin)
    schedule.every().day.at("18:00").do(scheduler.process_next_pin)
    schedule.every().day.at("19:00").do(scheduler.process_next_pin)

    logger.info("Pinterest Scheduler started")
    
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main()