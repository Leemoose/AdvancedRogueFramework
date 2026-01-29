
class MessageHandler():

    def __init__(self):
        self.messages = []
        self.message_display = ""

    def add_message(self, message, color = (255,255,255)):
        if len(self.messages) >= 5:
            self.messages.pop(0)
        self.messages.append((message, color))
        self.set_message_display()

    def clear_message(self):
        self.messages = []

    def set_message_display(self):
        text = "".join([message[0] + "<br>" for message in (self.get_messages())])
        text = text[:-4] #Remove last <br>
        self.message_display = text

    def get_messages(self):
        return self.messages

    def get_message_display(self):
        return self.message_display