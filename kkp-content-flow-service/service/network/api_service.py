import requests

class ApiService:
    def __init__(self, api_key):
        self.api_key = api_key

    def post(self, url, payload):
        headers = {
            "X-API-Key": self.api_key,
            "Content-Type": "application/json"
        }
        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while posting to the API: {e}")
            return None