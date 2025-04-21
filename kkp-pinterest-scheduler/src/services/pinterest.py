import os
from pinterest.client import PinterestSDKClient
from pinterest.organic.pins import Pin as PinterestPin
from dotenv import load_dotenv
import base64
import sys

load_dotenv()

class PinterestService:
    def __init__(self):
        print("Initializing PinterestService")
        try:
            # Get access token from environment
            access_token = os.getenv('PINTEREST_ACCESS_TOKEN')
            if not access_token:
                print("ERROR: PINTEREST_ACCESS_TOKEN not found in environment variables")
                print("Please add your Pinterest access token to the .env file")
                print("Example: PINTEREST_ACCESS_TOKEN=your_token_here")
                sys.exit(1)
            
            print("Creating Pinterest client with access token")
            # Create the client with the access token
            self.client = PinterestSDKClient.create_client_with_token(access_token)
            print("Pinterest client initialized successfully")
                
        except Exception as e:
            print(f"Error initializing Pinterest client: {str(e)}")
            raise

    def create_pin(self, pin):
        """
        Create a pin on Pinterest
        """
        try:
            print(f"Creating pin with title: {pin.title}")
            
            # Verify the image file exists
            if not os.path.exists(pin.image_path):
                raise FileNotFoundError(f"Image file not found: {pin.image_path}")
            
            print("Image file exists, reading and encoding...")
            # Read and encode the image
            with open(pin.image_path, "rb") as image_file:
                base64_image = base64.b64encode(image_file.read()).decode('utf-8')
            
            print("Creating pin on Pinterest...")
            # Create the pin using the SDK
            pinterest_pin = PinterestPin.create(
                board_id=pin.board_id,
                media_source={
                    "source_type": "image_base64",
                    "content_type": "image/jpeg",
                    "data": base64_image
                },
                title=pin.title,
                description=pin.description,
                link=pin.link,
                client=self.client
            )
            
            print(f"Pin created successfully with ID: {pinterest_pin.id}")
            return pinterest_pin
            
        except Exception as e:
            print(f"Error creating pin: {str(e)}")
            if "Authentication failed" in str(e):
                print("\nAuthentication Error: Your Pinterest access token is invalid or expired.")
                print("Please generate a new access token from the Pinterest Developer Portal")
                print("and update your .env file with the new token.")
            raise