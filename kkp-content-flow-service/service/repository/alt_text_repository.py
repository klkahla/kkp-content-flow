# kkp-content-flow-service/service/alt_text_repository.py


class AltTextRepository:
    def __init__(self, api_service, api_url):
        self.api_service = api_service
        self.api_url = api_url

    def create_image(self, image_base64, tags):
        payload = {
            "image": {
                "raw": image_base64,
                "tags": tags
            },
        }
        return self.api_service.post(self.api_url, payload)