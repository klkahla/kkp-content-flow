import schedule
import time
from datetime import datetime
from src.models.pin import Session, Pin
from src.services.pinterest import PinterestService
from src.services.email_service import EmailService
from src.services.csv_handler import CSVHandler
from src.utils.logger import logger
from dotenv import load_dotenv
import os

load_dotenv()

class PinterestScheduler:
    def __init__(self):
        self.pinterest_service = PinterestService()
        self.session = Session()
        self.email_service = EmailService()
    def process_next_pin(self):
        """
        Process the oldest pending pin
        """
        try:
            # Get the oldest pending pin
            pin = self.session.query(Pin)\
                .order_by(Pin.created_at.asc())\
                .first()

            if not pin:
                logger.info("No pending pins found")
                return

            # Create pin on Pinterest
            self.pinterest_service.create_pin(pin)

            # Delete the image file from Raspberry Pi if it exists
            if os.path.exists(pin.image_path):
                os.remove(pin.image_path)
                logger.info(f"Deleted image file: {pin.image_path}")

            # Delete the pin from database
            self.session.delete(pin)
            self.session.commit()
            logger.info(f"Successfully posted and deleted pin: {pin.title}")

        except Exception as e:
            logger.error(f"Error processing pin: {str(e)}")
            if pin:
                pin.status = 'failed'
                self.session.commit()
                # try:
                #     self.email_service.send_failure_notification(pin, str(e))
                # except Exception as email_error:
                #     logger.error(f"Failed to send email notification: {str(email_error)}")
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