# Goal: Parse channel portion of SpikeSafe get status into an accessible object
# Example: (CH1 10.123456 1.123000 1)

import math

class ChannelData():

    channel_number = 0

    current_reading = math.nan

    is_on_state = False

    voltage_reading = math.nan

    def __init__(self):
        pass

    # Goal: Helper function to parse channel portion of SpikeSafe get status into an accessible object
    def ParseChannelData(self, channel_get_status_response):
        try:
            # find start of CH, extract "1 10.123456 1.123000 1" to string, and separate by " " into list
            search_str = b"CH"
            channel_data_start_index = channel_get_status_response.find(search_str)
            channel_parsable_format = channel_get_status_response[channel_data_start_index + len(search_str) : len(channel_get_status_response) - 1]
            channel_response_split = channel_parsable_format.split(b' ')

            # set all values
            self.channel_number = int(channel_response_split[0])
            self.voltage_reading = float(channel_response_split[1])
            self.current_reading = float(channel_response_split[2])
            self.is_on_state = {b'0': False, b'1': True}[channel_response_split[3]]

            # return channel data object to caller
            return self
        except Exception as err:
            # print any error to terminal and raise to function caller
            print("Error parsing channel data from SpikeSafe get status: {}".format(err))                                            
            raise  