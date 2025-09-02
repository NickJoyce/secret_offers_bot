import requests
import logging
import base64
import json
from aiohttp import ClientSession


logger = logging.getLogger(__name__)



class Methods():
    def __init__(self, base_url):
        self.base_url = base_url

    def send_message_to_operator(self):
        return f"{self.base_url}/chat/message/sendToOperator"
    
    
class TalkMeApi():
    def __init__(self, base_url, token):
        self.base_url = base_url
        self.token = token
        self.methods = Methods(self.base_url)


    @property
    def headers(self):
        return {
            'Content-Type': 'application/json;charset=utf-8',
            'X-Token': self.token
        }
        
    async def send_message_to_operator(self, client_id: str, text: str):
        async with ClientSession() as session:
            data = {
                    "client": {
                        "id": client_id,
                        },
                    "message": {
                        "text": text
                    }
                }
            async with session.post(self.methods.send_message_to_operator(), headers=self.headers, json=data) as response:
                return await response.json()


    
    
