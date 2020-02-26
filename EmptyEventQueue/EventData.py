import math

class EventData():
    
    event_text = None

    code = 0

    message = None

    channel_list = []

    def __init__(self, event_text, code, message, channel_list):
        self.event_text = event_text
        self.code = code
        self.message = message
        self.channel_list = channel_list