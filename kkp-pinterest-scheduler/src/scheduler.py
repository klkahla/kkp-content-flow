from datetime import datetime
from models.pin import Session, Pin
from services.pinterest import PinterestService
from services.email_service import EmailService
from utils.logger import logger
from dotenv import load_dotenv
import os

print("Starting script")
load_dotenv()

print("Loaded environment variables")

class PinterestScheduler:
    def __init__(self):
        print("Initializing PinterestScheduler")
        self.pinterest_service = PinterestService()
        print("PinterestService initialized")
        self.session = Session()
        # self.email_service = EmailService()
    def process_next_pin(self):
        """
        Process the oldest pending pin
        """
        try:
            print("Starting to process next pin")
            # Get the oldest pending pin
            pin = self.session.query(Pin)\
                .order_by(Pin.created_at.asc())\
                .first()
            
            # Create a dummy pin for testing if no pin exists
            # pin = Pin(
            #     link="www.katykahlaphotography.com",
            #     title="Test Pin",
            #     description="This is a test pin",
            #     image_path="/Users/katykahla/Pictures/BusinessHeadshot/Finals/Instagram/kkahla-photography-2.jpg",
            #     board_id=os.getenv('PINTEREST_BOARD_ID_COUPLES')
            # )
            print(f"Pin: {pin}")

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
            print(f"Error processing pin: {str(e)}")
                # try:
                #     self.email_service.send_failure_notification(pin, str(e))
                # except Exception as email_error:
                #     logger.error(f"Failed to send email notification: {str(email_error)}")
        finally:
            self.session.close()
            pass

def main():
    print("Starting scheduler")
    scheduler = PinterestScheduler()

    # Time check
    current_time = datetime.now().strftime("%H:%M")
    # Convert current time to minutes since midnight for easier comparison
    current_hour, current_minute = map(int, current_time.split(':'))
    current_minutes = current_hour * 60 + current_minute
    print(f"Current time: {current_time}")
    print(f"Current minutes: {current_minutes}")

    # Define scheduled times in minutes since midnight
    scheduled_times = [360, 420, 720, 1080, 1140]  # 6am, 7am, 12pm, 6pm, 7pm

    scheduler.process_next_pin()

    # Check if current time is within 5 minutes of any scheduled time
    if any(abs(current_minutes - scheduled) <= 5 for scheduled in scheduled_times):
        logger.info(f"Processing next pin at {current_time}")
        print(f"Processing next pin at {current_time}")
        
    else:
        logger.info(f"Not valid time to process pin at {current_time}")
        print(f"Not valid time to process pin at {current_time}")

if __name__ == "__main__":
    main()