# Goal: Parse SpikeSafe get status into an accessible object
# Example status 1: (DIF (NAME "Output Readings" (DATA (BULK 99.7) (CH1 10.123456 1.123000 1) (T1 20.7) (T2 0.0) (T3 0.0) (T4 0.0) )))
# Example status 2: (DIF (NAME "Output Readings" (DATA (BULK 99.7) (CH1 10.123456 1.123000 1) (CH2 0.000000 0.000000 0) (T1 20.7) (T2 21.0) (T3 0.0) (T4 0.0) )))

import math
from GetStatus import ChannelData
from GetStatus import TemperatureData

class GetStatus():
    
    bulk_voltage = math.nan

    channel_data = []

    temperature_data = []

    def __init__(self):
        pass

    # Goal: Helper function to parse SpikeSafe get status into an accessible object
    def ParseGetStatus(self, get_status_response):
        self.bulk_voltage = self.__parseBulkVoltage__(get_status_response)
        self.channel_data = self.__parseAllChannelData__(get_status_response)
        self.temperature_data = self.__parseAllTemperatureData__(get_status_response)

        return self
    
    # Goal: Helper function to parse bulk votage SpikeSafe get status
    # e.g. parse "99.7" from examples in header
    def __parseBulkVoltage__(self, get_status_response):
        try:
            bulk_voltage = None
            # find start of BULK in get status response
            search_str = b"(BULK "
            bulk_start_index = get_status_response.find(search_str)

            # find first ) after BULK, extract bulk voltage string, and confirm float bulk voltage
            if bulk_start_index > -1: 
                bulk_parenthesis_end_index = get_status_response.find(b")", bulk_start_index)
                bulk_voltage_str = get_status_response[bulk_start_index + len(search_str) : bulk_parenthesis_end_index]

                if isinstance(float(bulk_voltage_str), float) == True:                                      
                    bulk_voltage = float(bulk_voltage_str)           

            # unexpected bulk voltage detected from SpikeSafe, end parsing
            if bulk_voltage == None:                                                                        
                raise Exception('Could not parse bulk voltage from: {}'.format(get_status_response))

            return bulk_voltage

        except Exception as err:
            # print any error to terminal and raise to function caller
            print("Error parsing bulk voltage: {}".format(err))                                            
            raise  
    
    # Goal: Helper function to parse channel data from SpikeSafe get status
    # e.g. (CH1 10.123456 1.123000 1) (CH2 0.000000 0.000000 0) from examples in header
    def __parseAllChannelData__(self, get_status_response):
        try:
            channel_data_list = []

            # initialize flag to check if channel data is found
            channel_data_found = True

            # initialize position of last channel data found
            last_channel_data_start_index = 0

            # run as long as channel data is found
            while channel_data_found == True:
                # search for the next channel data after the last channel data position
                search_str = b"(CH"
                channel_data_start_index = get_status_response.find(search_str, last_channel_data_start_index)

                if channel_data_start_index != -1:
                    # look for the end of the channel data, parse it into an object, add it to list, and continue search
                    channel_data_end_index = get_status_response.find(b")", channel_data_start_index)
                    channel_data_str = get_status_response[channel_data_start_index - 1:channel_data_end_index + 1]
                    channel_data = ChannelData.ChannelData().ParseChannelData(channel_data_str)
                    channel_data_list.append(channel_data)
                    last_channel_data_start_index = channel_data_start_index + len(search_str)
                else:
                    # Stop search when all channel data is found
                    channel_data_found = False

            # return channel data list to caller
            return channel_data_list
        except Exception as err:
            # print any error to terminal and raise to function caller
            print("Error parsing channel status: {}".format(err))
            raise

    # Goal: Helper function to parse temperature data from SpikeSafe get status
    # e.g. (T1 20.7) (T2 0.0) from examples in header
    def __parseAllTemperatureData__(self, get_status_response):
        try:
            temperature_data_list = []

            # initialize flag to check if temperature data is found
            temperature_data_found = True

            # initialize position of last temperature data found
            last_temperature_data_start_index = 0

            # run as long as temperature data is found
            while temperature_data_found == True:
                # search for the next temperature data after the last temperature data position
                search_str = b"(T"
                temperature_data_start_index = get_status_response.find(search_str, last_temperature_data_start_index)

                if temperature_data_start_index != -1:
                    # look for the end of the temperature data, parse it into an object, add it to list, and continue search
                    temperature_data_end_index = get_status_response.find(b")", temperature_data_start_index)
                    temperature_data_str = get_status_response[temperature_data_start_index - 1:temperature_data_end_index + 1]
                    temperature_data = TemperatureData.TemperatureData().ParseTemperatureData(temperature_data_str)
                    temperature_data_list.append(temperature_data)
                    last_temperature_data_start_index = temperature_data_start_index + len(search_str)
                else:
                    # Stop search when all temperature data is found
                    temperature_data_found = False

            # return temperature data list to caller
            return temperature_data_list
        except Exception as err:
            # print any error to terminal and raise to function caller
            print("Error parsing temperature status: {}".format(err))
            raise   