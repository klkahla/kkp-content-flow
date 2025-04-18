import os
from pinterest.client import PinterestAPI
from dotenv import load_dotenv
import base64
load_dotenv()

class PinterestService:
    def __init__(self):
        self.api = PinterestAPI(
            access_token=os.getenv('PINTEREST_ACCESS_TOKEN')
        )

    def create_pin(self, pin):
        """
        Create a pin on Pinterest
        """
        try:
           
            with open(pin.image_path, "rb") as image_file:
                base64_image = base64.b64encode(image_file.read()).decode('utf-8')

            # TODO: format the pin data for posting to Pinterest
            response = self.api.pins.create(
                board=pin.board_id,
                media_source={
                    "source_type": "image_base64",
                    "content_type": "image/jpeg",
                    "data": base64_image
                },
                title=pin.title,
                description=pin.description,
                link=pin.link
            )
            return response
        except Exception as e:
            print(f"Error creating pin: {str(e)}")
            raise