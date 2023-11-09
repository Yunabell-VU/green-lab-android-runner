import json
import os.path
import random
import time
from telethon import TelegramClient, sync
import argparse

# These example values won't work. You must get your own api_id and
# api_hash from https://my.telegram.org, under API Development.


with open(os.path.dirname(os.path.abspath(__file__)) + '/config.json', 'r') as json_file:
    parser = argparse.ArgumentParser()
    # for the initial py script
    parser.add_argument('file')
    parser.add_argument('--progress', action='store')
    # for this py script
    parser.add_argument('--nr_of_messages', action='store')
    parser.add_argument('--burst', action='store_true')
    arg: argparse.Namespace = parser.parse_args()
    data = json.load(json_file)
    api_id = data["api_id"]
    api_hash = data["api_hash"]
    session_name = data["session_name"]
    receiver = data["receiver"]
    messages = data["messages"]
    nr_of_messages = data["nr_of_messages"]
    sending_window = data["sending_window"]
    setup_time = data["setup_time"]
    receiving_buffer = data["receiving_buffer"]
    burst = data["burst"]
    # command-line arguments override the corresponding entries in config.json
    try:
        nr_of_messages = int(arg.nr_of_messages)
    except:
        pass
    try:
        burst = arg.burst
    except:
        pass

client = TelegramClient(session_name, api_id, api_hash).start()


def send_message():
    message = random.choice(messages)
    message = "[" + time.strftime(" at %H:%M:%S", time.localtime()) + "] " + message
    client.send_message(receiver, message)
    print(message)


def auto_sending():
    if nr_of_messages == 0:
        time.sleep(sending_window)
    else:
        if burst:
            send_interval = 0.2
        else:
            send_interval = sending_window / nr_of_messages
        for _ in range(nr_of_messages):
            send_message()
            time.sleep(send_interval)
        if burst:
            time.sleep(sending_window - send_interval * nr_of_messages)  # make burst / even message sending consume the same time period


def repeat_auto_sending():
    time.sleep(setup_time)
    auto_sending()
    time.sleep(receiving_buffer)


def main():
    print("sending messages to ====> " + receiver)
    repeat_auto_sending()


if __name__ == "__main__":
    main()
