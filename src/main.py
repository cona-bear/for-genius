import datetime
import os
import random
import time

import pytz
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from webdriver_manager.chrome import ChromeDriverManager

SLACK_TOKEN = os.getenv("SLACK_BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")


def get_random_problem():
    """Fetches a random problem url from the NeetCode 150 website.

    @deprecated

    Example:
        problem_url = get_random_problem()
        print(problem_url)
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get("https://neetcode.io/practice?tab=neetcode150")
        time.sleep(5)  # Wait for JavaScript to load the pagei

        section_buttons = driver.find_elements(
            By.CSS_SELECTOR, "button.accordion.button"
        )
        for button in section_buttons:
            try:
                button.click()
                time.sleep(1)  # Small delay to allow content to load
            except:
                print("Skipping button (possibly already expanded)")

        time.sleep(2)  # Ensure all sections are expanded)

        problem_elements = driver.find_elements(
            By.CSS_SELECTOR, "a[href^='/problems/']"
        )
        problems = [
            {"title": el.text.strip(), "url": el.get_attribute("href")}
            for el in problem_elements
            if el.text.strip()
        ]

        driver.quit()

        if not problems:
            return "No problems found."

        problem = random.choice(problems)
        return problem

    except Exception as e:
        driver.quit()
        return f"Error: {str(e)}"


def build_message():
    kst = pytz.timezone("Asia/Seoul")
    today = datetime.datetime.now(kst).strftime("%m/%d")
    seed = datetime.datetime.now(kst).strftime("%Y%m%d")

    return [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": f"{today} Hello Genius! What do you call a bear without ears?",
            },
        },
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {"type": "plain_text", "text": ":capital_abcd: Wordle"},
                    "url": "https://www.nytimes.com/games/wordle",
                },
                {
                    "type": "button",
                    "text": {"type": "plain_text", "text": ":jigsaw: 꼬들"},
                    "url": "https://kordle.kr",
                },
                {
                    "type": "button",
                    "text": {"type": "plain_text", "text": ":ms_windows: Quordle"},
                    "url": "https://www.merriam-webster.com/games/quordle",
                },
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": ":maru_is_a_puppy: Numberle",
                    },
                    "url": f"https://numberle.org/?seed={seed}",
                },
                {
                    "type": "button",
                    "text": {"type": "plain_text", "text": ":10_10: Contexto"},
                    "url": "https://contexto.me/",
                },
                {
                    "type": "button",
                    "text": {"type": "plain_text", "text": ":waffle: Waffle"},
                    "url": "https://wafflegame.net/",
                },
            ],
        },
    ]


if __name__ == "__main__":
    client = WebClient(token=SLACK_TOKEN)

    try:
        response = client.chat_postMessage(
            channel=CHANNEL_ID,
            blocks=build_message(),
            unfurl_links=False,  # Don't show preview of the link
            text="If you see this message, please check the bot's configuration.",
        )
        print(f"chat_postMessage: response={response}")
    except SlackApiError as e:
        assert e.response["error"]
