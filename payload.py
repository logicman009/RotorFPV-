import time


class PayloadSystem:
    def __init__(self):
        self.released = False

    def drop_payload(self):
        print("Dropping payload")

        time.sleep(1)

        self.released = True

        print("Payload released")
