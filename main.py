import inspect
import re
import time
from typing import Dict, List, Optional, Tuple

from slackclient import SlackClient  # type: ignore

from config import BOT_NAME, BOT_TOKEN, AT_BOT
from primitives import SlackMessage


def handle_command(slack_message: SlackMessage, slack_client: SlackClient) -> None:
    response = ("```\n" + inspect.getdoc(slack_message.text) + "\n```"
                if slack_message.text is not None
                else "Sorry, I couldn't handle that")
    slack_client.api_call("chat.postMessage",
                          channel=slack_message.channel,
                          text=response,
                          as_user=True)

def parse_helper(response: str) -> Optional[str]:
        return (re.match(r"help\((?P<help_input>.*?)\)",
                         response).group("help_input")
                if response is not None else None)


def parse_slack_output(slack_rtm_output: List[Dict[str, str]]) -> SlackMessage:
    print(slack_rtm_output)
    in_text = slack_rtm_output[0].get("text") if slack_rtm_output else None
    channel = slack_rtm_output[0].get("channel") if slack_rtm_output else None
    return SlackMessage(in_text, channel)


def main(bot_name: str=BOT_NAME,
         bot_token: str=BOT_TOKEN):
    slack_client = SlackClient(bot_token)
    if slack_client.rtm_connect():
        print("Connected!")
        while True:
            slack_message = parse_slack_output(slack_client.rtm_read())
            print(parse_helper(slack_message.text))
            handle_command(slack_message, slack_client)
            time.sleep(1)
    else:
        print("Connection failed")

if __name__ == '__main__':
    main()
