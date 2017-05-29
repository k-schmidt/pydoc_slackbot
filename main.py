import inspect
import time

from slackclient import SlackClient

from config import BOT_NAME, BOT_TOKEN, AT_BOT


def handle_command(command, channel, slack_client):
    response = inspect.getdoc(command)
    slack_client.api_call("chat.postMessage",
                          channel=channel,
                          text=response,
                          as_user=True)

def parse_slack_output(slack_rtm_output):
    in_text = slack_rtm_output[0].get("text") if slack_rtm_output else None
    channel = slack_rtm_output[0].get("channel") if slack_rtm_output else None
    print(in_text, channel)
    if in_text and channel and AT_BOT in in_text:
        response = (in_text.split(AT_BOT)[1].strip().lower())
        return (response, channel)
    return None, None


def main(bot_name=BOT_NAME,
         bot_token=BOT_TOKEN):
    slack_client = SlackClient(bot_token)
    if slack_client.rtm_connect():
        print("Connected!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel, slack_client)
            time.sleep(1)
    else:
        print("Connection failed")

if __name__ == '__main__':
    main()
