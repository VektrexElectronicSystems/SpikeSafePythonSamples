import math

class ChannelData():

    channel_number = 0

    current_reading = math.nan

    is_on_state = False

    voltage_reading = math.nan

    def __init__(self):
        pass

    # Goal: Parse channel portion of SpikeSafe get status into an accessible object
    # Example: (CH1 10.123456 1.123000 1)
    def ParseChannelData(self, channel_get_status_response):
        # self.channel_number = self.__parseChannelNumber__(channel_get_status_response)
        # self.current_reading = self.__parseChannelCurrentReading__(channel_get_status_response)
        # self.is_on_state = self.__parseChannelIsOnState__(channel_get_status_response)
        # self.voltage_reading = self.__parseChannelVoltageReading__(channel_get_status_response)

        # find start of CH, extract "1 10.123456 1.123000 1" to string, and separate by " " into list
        search_str = b"CH"
        channel_data_start_index = channel_get_status_response.find(search_str)
        channel_parsable_format = channel_get_status_response[channel_data_start_index + len(search_str) : len(channel_get_status_response) - 1]
        channel_response_split = channel_parsable_format.split(b' ')

        # set all values
        if len(channel_response_split) == 4:
            self.channel = int(channel_response_split[0])
            self.voltage_reading = float(channel_response_split[1])
            self.current_reading = float(channel_response_split[2])
            self.is_on_state = {b'0': False, b'1': True}[channel_response_split[3]]
        else:
            # unexpected channel portion from SpikeSafe get status, end parsing
            raise Exception('Could not parse channel number from: {}'.format(channel_get_status_response))

        return self

    # # Goal: Helper function parse channel number from channel get status
    # # Example: parse "1" from "CH1" from (CH1 10.123456 1.123000 1)
    # def __parseChannelNumber__(self, channel_get_status_response):
    #     try:
    #         channel_number = None

    #         if channel_number == None:  
    #             # unexpected channel number detected from SpikeSafe get status, end parsing
    #             raise Exception('Could not parse channel number from: {}'.format(channel_get_status_response))

    #         return channel_number
    #     except Exception as err:
    #         # print any error to terminal and raise error to function caller
    #         print("Error parsing channel number: {}".format(err))   
    #         raise
    
    # # Goal: Helper function parse current reading from channel get status
    # # Example: parse "1.123000" from (CH1 10.123456 1.123000 1)
    # def __parseChannelCurrentReading__(self, channel_get_status_response):
    #     try:
    #         current_reading = None

    #         if current_reading == None:  
    #             # unexpected current reading detected from SpikeSafe get status, end parsing
    #             raise Exception('Could not parse current reading from: {}'.format(channel_get_status_response))

    #         return current_reading
    #     except Exception as err:
    #         # print any error to terminal and raise error to function caller
    #         print("Error parsing channel current reading: {}".format(err))   
    #         raise

    # # Goal: Helper function parse is on state from channel get status
    # # Example: parse "1" from (CH1 10.123456 1.123000 1)
    # def __parseChannelIsOnState__(self, channel_get_status_response):
    #     try:
    #         is_on_state = None

    #         if is_on_state == None:  
    #             # unexpected is on state detected from SpikeSafe get status, end parsing
    #             raise Exception('Could not parse is on state from: {}'.format(channel_get_status_response))

    #         return is_on_state
    #     except Exception as err:
    #         # print any error to terminal and raise error to function caller
    #         print("Error parsing channel is on state: {}".format(err))   
    #         raise

    # # Goal: Helper function parse voltage reading from channel get status
    # # Example: parse "10.123456" from (CH1 10.123456 1.123000 1)
    # def __parseChannelVoltageReading__(self, channel_get_status_response):
    #     try:
    #         voltage_reading = None

    #         if voltage_reading == None:  
    #             # unexpected voltage reading detected from SpikeSafe get status, end parsing
    #             raise Exception('Could not parse voltage reading state from: {}'.format(channel_get_status_response))

    #         return voltage_reading
    #     except Exception as err:
    #         # print any error to terminal and raise error to function caller
    #         print("Error parsing channel voltage reading: {}".format(err))   
    #         raise         