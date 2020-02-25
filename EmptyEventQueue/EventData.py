import math

class EventData():
    
    code = 0

    message = ''

    channel_list = []

    def __init__(self, code, message, channel_list):
        self.code = code
        self.message = message
        self.channel_list = channel_list