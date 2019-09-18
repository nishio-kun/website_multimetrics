import os

from dotenv import load_dotenv


load_dotenv()

ACCESS_TOKEN_PUBLISH_URL = os.environ['ACCESS_TOKEN_PUBLISH_URL']
DEVELOPER_API_BASE_URL = os.environ['DEVELOPER_API_BASE_URL']
DEVELOPER_CLIENT_ID = os.environ['DEVELOPER_CLIENT_ID']
DEVELOPER_CLIENT_SECRET = os.environ['DEVELOPER_CLIENT_SECRET']
HOST = os.environ['HOST']
