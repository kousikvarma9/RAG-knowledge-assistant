import json
import os

CHAT_HISTORY_PATH = "data/chat_history.json"


class ChatHistory:

    @staticmethod
    def load():

        if not os.path.exists(
            CHAT_HISTORY_PATH
        ):
            return []

        with open(
            CHAT_HISTORY_PATH,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    @staticmethod
    def save(history):

        with open(
            CHAT_HISTORY_PATH,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                history,
                f,
                indent=4
            )