import os
import pytz 
import datetime

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


SLACK_TOKEN = os.getenv("SLACK_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")


def build_message():

    kst = pytz.timezone("Asia/Seoul")
    today = datetime.datetime.now(kst).strftime("%m/%d")

    return [{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": f":maru_is_a_puppy: {today} Today's Brain Exercise :maru_is_a_puppy:"
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "Hey Genius, *BRING IT ON!!!!!*"
			}
		},
		{
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": ":capital_abcd: WORDLE"
					},
					"url": "https://www.nytimes.com/games/wordle"
				},
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": ":jigsaw: 꼬들"
					},
					"url": "https://kordle.kr"
				},
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": ":quad_parrot: Quordle"
					},
					"url": "https://www.merriam-webster.com/games/quordle"
				},
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": ":10_10: Contexto"
					},
					"url": "https://contexto.me/"
				},
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": ":waffle: Waffle"
					},
					"url": "https://wafflegame.net/"
				}
			]
		},
		{
			"type": "divider"
		},
		{
			"type": "section",
			"text": {
				"type": "plain_text",
				"text": "maru luvs you. maru is a puppy. :maru_heart:",
			}
		},
    ]


if __name__ == "__main__":
    client = WebClient(token=SLACK_TOKEN)
    
    try:
        response = client.chat_postMessage(
            channel=CHANNEL_ID,
            blocks=build_message(),
            unfurl_links=False, # Don't show preview of the link
        )
    except SlackApiError as e:
        assert e.response["error"]
