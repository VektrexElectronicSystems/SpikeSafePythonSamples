# Goal: Parse SpikeSafe memory table read into an accessible object
# Example memory table read 1: (DIF (NAME "Output Readings" (DATA (BULK 99.7) (CH1 10.123456 1.123000 1) (T1 20.7) (T2 0.0) (T3 0.0) (T4 0.0) )))
# Example memory table read 2: (DIF (NAME "Output Readings" (DATA (BULK 99.7) (CH1 10.123456 1.123000 1) (CH2 0.000000 0.000000 0) (T1 20.7) (T2 21.0) (T3 0.0) (T4 0.0) )))

import math
from Data.ChannelData import ChannelData
from Data.TemperatureData import TemperatureData

class MemoryTableReadData():
    
    bulk_voltage = math.nan

    channel_data = []

    temperature_data = []

    def __init__(self):
        pass

    # Goal: Helper function to parse SpikeSafe memory table read into an accessible object
    def ParseMemoryTableRead(self, get_memory_table_read_response):
        self.bulk_voltage = self.__parseBulkVoltage__(get_memory_table_read_response)
        self.channel_data = self.__parseAllChannelData__(get_memory_table_read_response)
        self.temperature_data = self.__parseAllTemperatureData__(get_memory_table_read_response)

        # return memory table read object to caller
        return self
    
    # Goal: Helper function to parse bulk votage SpikeSafe memory table read
    # e.g. parse "99.7" from examples in header
    def __parseBulkVoltage__(self, get_memory_table_read_response):
        try:
            bulk_voltage = None
            # find start of BULK in memory table read response
            search_str = b"(BULK "
            bulk_start_index = get_memory_table_read_response.find(search_str)

            # find first ) after BULK, extract bulk voltage string, and set float bulk voltage
            bulk_parenthesis_end_index = get_memory_table_read_response.find(b")", bulk_start_index)
            bulk_voltage_str = get_memory_table_read_response[bulk_start_index + len(search_str) : bulk_parenthesis_end_index]
            bulk_voltage = float(bulk_voltage_str)           

            # return bulk voltage to caller
            return bulk_voltage
        except Exception as err:
            # print any error to terminal and raise to function caller
            print("Error parsing bulk voltage from memory table read: {}".format(err))                                            
            raise  
    
    # Goal: Helper function to parse channel data from SpikeSafe memory table read
    # e.g. (CH1 10.123456 1.123000 1) (CH2 0.000000 0.000000 0) from examples in header
    def __parseAllChannelData__(self, get_memory_table_read_response):
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
                channel_data_start_index = get_memory_table_read_response.find(search_str, last_channel_data_start_index)

                if channel_data_start_index != -1:
                    # look for the end of the channel data, parse it into an object, add it to list, and continue search
                    channel_data_end_index = get_memory_table_read_response.find(b")", channel_data_start_index)
                    channel_data_str = get_memory_table_read_response[channel_data_start_index - 1:channel_data_end_index + 1]
                    channel_data = ChannelData().ParseChannelData(channel_data_str)
                    channel_data_list.append(channel_data)
                    last_channel_data_start_index = channel_data_start_index + len(search_str)
                else:
                    # Stop search when all channel data is found
                    channel_data_found = False

            # return channel data list to caller
            return channel_data_list
        except Exception as err:
            # print any error to terminal and raise to function caller
            print("Error parsing channel from memory table read: {}".format(err))
            raise

    # Goal: Helper function to parse temperature data from SpikeSafe memory table read
    # e.g. (T1 20.7) (T2 0.0) from examples in header
    def __parseAllTemperatureData__(self, get_memory_table_read_response):
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
                temperature_data_start_index = get_memory_table_read_response.find(search_str, last_temperature_data_start_index)

                if temperature_data_start_index != -1:
                    # look for the end of the temperature data, parse it into an object, add it to list, and continue search
                    temperature_data_end_index = get_memory_table_read_response.find(b")", temperature_data_start_index)
                    temperature_data_str = get_memory_table_read_response[temperature_data_start_index - 1:temperature_data_end_index + 1]
                    temperature_data = TemperatureData().ParseTemperatureData(temperature_data_str)
                    temperature_data_list.append(temperature_data)
                    last_temperature_data_start_index = temperature_data_start_index + len(search_str)
                else:
                    # Stop search when all temperature data is found
                    temperature_data_found = False

            # return temperature data list to caller
            return temperature_data_list
        except Exception as err:
            # print any error to terminal and raise to function caller
            print("Error parsing temperature from memory table read: {}".format(err))
            raise

def LogMemoryTableRead(spike_safe_socket):
    spike_safe_socket.sendScpiCommand('MEM:TABL:READ') # request SpikeSafe memory table
    data = spike_safe_socket.readData()                # read SpikeSafe memory table
    print(data)   