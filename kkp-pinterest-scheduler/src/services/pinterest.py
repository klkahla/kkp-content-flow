import os
from pinterest.client import PinterestAPI
from dotenv import load_dotenv

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
            response = self.api.pins.create(
                board=pin.board,
                media_source={
                    "source_type": "image_url",
                    "url": pin.image_path
                },
                title=pin.title,
                description=pin.description
            )
            return response
        except Exception as e:
            print(f"Error creating pin: {str(e)}")
            raise