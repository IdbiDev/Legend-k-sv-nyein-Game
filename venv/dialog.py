import keyboard
import time

class Dialog:
    def __init__(self, text: str, is_fast = False):
        self.text = text
        self.is_fast = is_fast

    def is_running(self) -> bool:
        return self.is_running


    def print(self):
        self.text_buffer = ""
        self.skip = False
        self.is_running = False
        for x in self.text:
            if keyboard.is_pressed("space"):
                self.skip = True
            self.is_running = True
            self.text_buffer += x
            if self.skip:
                break
            print("\r" + self.text_buffer, end="")
            time.sleep(0.05)

        print("\r" + self.text, end="")

        self.is_running = False
        print()
        if not self.is_fast:
            if self.skip:
                time.sleep(1)
            else:
                time.sleep(2)


