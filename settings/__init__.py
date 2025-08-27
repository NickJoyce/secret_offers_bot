import os
from dotenv import load_dotenv

load_dotenv()

if os.getenv('ENV_TYPE') == 'dev':
    from .dev import *
elif os.getenv('ENV_TYPE') == 'prod':
    from .prod import *
else:
    raise Exception(f"the ENV_TYPE environment variable is not defined in .env file, it must be 'dev' or 'prod'")