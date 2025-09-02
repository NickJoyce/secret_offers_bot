from .lib import TalkMeApi
from settings import TALK_ME_API_BASE_URL, TALK_ME_API_TOKEN

talk_me = TalkMeApi(base_url=TALK_ME_API_BASE_URL, token=TALK_ME_API_TOKEN)
