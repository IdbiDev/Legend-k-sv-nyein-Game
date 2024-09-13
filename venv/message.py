import json
import random
from dialog import Dialog

class Message:
    def __init__(self, name):
        self.name = name
        self.messages = []
        self.load_messages()


    def load_messages(self):
        with open('chat_messages.json', encoding="utf-8") as f:
            for msg in json.load(f)["messages"]:
                if msg["name"] == self.name:
                    for m in msg["messages"]:
                        self.messages.append(m)


    def get_message(self):
        msg = random.choice(self.messages) if isinstance(self.messages, list) else self.messages
        return msg


    def get_dialog_replaced_message(self, **kwargs):
        return Dialog(self.get_replaced_message(**kwargs))


    def get_dialog_message(self):
        return Dialog(random.choice(self.messages) if isinstance(self.messages, list) else self.messages)

    def get_replaced_message(self, **kwargs):
        modified_text = self.get_message()
        for target, replacement in kwargs.items():
            modified_text = modified_text.replace(f"%{target}%", replacement)
        return modified_text

    # def get_message(self, player_name, mob_name):
    #     msg = random.choice(self.messages) if isinstance(self.messages, list) else self.messages
    #     return Dialog(msg.replace("%player%", player_name).replace("%mob%", mob_name))
