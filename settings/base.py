import os
from pathlib import Path

SERVICE_NAME = 'secret_offers_bot'

BASE_DIR = Path(__file__).resolve().parent.parent

# logs
LOGS_DIR = Path(__file__).resolve().parent.parent.parent

# templates
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')

# database
DATABASE = os.getenv('DB_NAME')
USERNAME = os.getenv('DB_USER')
PASSWORD = os.getenv('DB_PASSWORD')
HOST = os.getenv('DB_HOST')
PORT = os.getenv('DB_PORT')

# sqlalchemy
SQLALCHEMY_DIALECT = 'postgresql'
SQLALCHEMY_DRIVER = 'asyncpg'
SQLALCHEMY_URL = f"{SQLALCHEMY_DIALECT}+{SQLALCHEMY_DRIVER}://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"

# alembic
ALEMBIC_DIALECT = SQLALCHEMY_DIALECT
ALEMBIC_SQLALCHEMY_URL = f"{ALEMBIC_DIALECT}://{USERNAME}:{PASSWORD}@{HOST}/{DATABASE}"

# Admin panel
ADMIN_SECRET = os.getenv('ADMIN_SECRET')
ADMIN_TOKEN = os.getenv('ADMIN_TOKEN')

# tg
TG_BOT_TOKEN = os.getenv('TG_BOT_TOKEN')
TG_ADMIN_ID = os.getenv('TG_ADMIN_ID')
WEBHOOK_SECRET = os.getenv('WEBHOOK_SECRET')

# elasticsearch
ES_BASE_URL = 'https://elasticsearch.podrugeapi.ru'
ES_USER = os.getenv('ES_USER')
ES_PASSWORD = os.getenv('ES_PASSWORD')



BASE_WEBHOOK_URL = "https://secret-offers-bot.podrugeapi.ru"

# tg webhook
# Path to webhook route, on which Telegram will send requests
WEBHOOK_PATH = "/webhook"
# Secret key to validate requests from Telegram (optional)
WEBHOOK_SECRET = os.getenv('WEBHOOK_SECRET')




# talk-me webhook
TALK_ME_WEBHOOK_LOGIN = os.getenv('TALK_ME_WEBHOOK_LOGIN')
TALK_ME_WEBHOOK_PASSWORD = os.getenv('TALK_ME_WEBHOOK_PASSWORD')
TALK_ME_BASE_WEBHOOKS_PATH = "/talk-me/webhooks"


# talk-me api
TALK_ME_API_BASE_URL = os.getenv('TALK_ME_API_BASE_URL')
TALK_ME_API_TOKEN = os.getenv('TALK_ME_API_TOKEN')



# authentication
IS_AUTH = True

# talk-me API
TALK_ME_BASE_URL = os.getenv('TALK_ME_BASE_URL', 'https://api.talk-me.com')
TALK_ME_API_KEY = os.getenv('TALK_ME_API_KEY')