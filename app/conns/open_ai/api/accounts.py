from .lib import GPTApi
from settings import GPT_API_KEY, GPT_BASE_URL


gpt = GPTApi(api_key=GPT_API_KEY, base_url=GPT_BASE_URL)

