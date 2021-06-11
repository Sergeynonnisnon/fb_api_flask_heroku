"""create by Sergey Tokarev nonnisnon@gmail.com"""
import os
from dotenv import load_dotenv
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

FB_access_token = os.environ.get('FB_access_token')
FB_id_groop = os.environ.get('FB_id_groop')
FB_app_secret = os.environ.get('FB_app_secret')
FB_app_id = os.environ.get('FB_app_id')
creator_post_skip = os.environ.get('creator_post_skip')
chanelSlack = os.environ.get('chanelSlack')
api_bot_secret_Slack = os.environ.get('api_bot_secret_Slack')
