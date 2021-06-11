from slack_sdk import WebClient

from settings import api_bot_secret_Slack

class Bot:
    BASE_message = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": (" "
            ),
        },
    }

    def __init__(self, channel):
        self.channel = channel

    def _mutable_msg_to_comment(self, namegroop, link):

        text = f'{namegroop}, {link}'
        return {"type": "section", "text": {"type": "mrkdwn", "text": f'новый коментарий в группе {text}'}},

    def _mutable_msg_to_post(self, namegroop, link):

        text = f'{namegroop}, {link}'
        return {"type": "section", "text": {"type": "mrkdwn", "text": f'новый пост в группе {text}'}},

    def get_message_new_comment(self,namegroop, link):
        return {
            "channel": self.channel,
            "blocks": [
                self.BASE_message,
                *self._mutable_msg_to_comment(namegroop, link),
            ],
        }

    def get_message_new_post(self,namegroop, link):
        return {
            "channel": self.channel,
            "blocks": [
                self.BASE_message,
                *self._mutable_msg_to_post(namegroop, link),
            ],
        }

    def send_msg_Slack_new_comment(self, namegroop='postoplan', link='https://www.facebook.com/groups/postoplan/'):
        slack_web_client = WebClient(api_bot_secret_Slack)

        message = self.get_message_new_comment(namegroop, link)

        slack_web_client.chat_postMessage(**message)

    def send_msg_Slack_new_post(self, namegroop='postoplan', link='https://www.facebook.com/groups/postoplan/'):
        slack_web_client = WebClient(api_bot_secret_Slack)

        message = self.get_message_new_post(namegroop, link)

        slack_web_client.chat_postMessage(**message)
