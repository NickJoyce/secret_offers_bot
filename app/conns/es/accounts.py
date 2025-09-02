from .lib import AsyncEsApi
from settings import ES_BASE_URL, ES_USER, ES_PASSWORD

es = AsyncEsApi(base_url=ES_BASE_URL, user=ES_USER, password=ES_PASSWORD)

