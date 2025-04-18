import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from src.utils.logger import logger

load_dotenv()

class EmailService:
    def __init__(self):
        self.recipient_email = os.getenv('RECIPIENT_EMAIL', 'kkahlaphotography@gmail.com')

    def send_failure_notification(self, pin, error_message):
        """
        Send email notification for failed pin
        """
        try:
            msg = MIMEMultipart()
            msg['From'] = self.recipient_email
            msg['To'] = self.recipient_email
            msg['Subject'] = f"Pinterest Pin Creation Failed: {pin.title}"

            body = f"""
            Pin creation failed for the following pin:
            
            Title: {pin.title}
            Description: {pin.description}
            Board: {pin.board}
            Image Path: {pin.image_path}
            
            Error: {error_message}
            
            Please check the logs for more details.
            """

            msg.attach(MIMEText(body, 'plain'))

            s = smtplib.SMTP('localhost')
            s.sendmail(self.recipient_email, [self.recipient_email], msg.as_string())
            s.quit()

            logger.info(f"Failure notification email sent for pin: {pin.title}")
        except Exception as e:
            logger.error(f"Failed to send email notification: {str(e)}")
            raise