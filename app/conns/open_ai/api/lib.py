from .methods import Methods
import requests

class GPTApi():
    def __init__(self, api_key: str, base_url: str):
        self.api_key = api_key
        self.methods = Methods(base_url)

    @property
    def headers(self):
        return {
            'Authorization': f"Bearer {self.api_key}",
            'Content-Type': 'application/json'
        }



    def create_a_model_response(self, body: dict):
        response = requests.post(url=self.methods.responses,
                                 headers=self.headers,
                                 json=body)
        return response.json()
