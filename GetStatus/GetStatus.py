import math
from GetStatus import ChannelData

class GetStatus():
    
    bulk_voltage = math.nan

    channel_data = []

    temperature_data = []

    def __init__(self):
        pass

    # Goal: Parse SpikeSafe get status into an accessible object
    # Example status 1: (DIF (NAME "Output Readings" (DATA (BULK 99.7) (CH1 10.123456 1.123000 1) (T1 20.7) (T2 0.0) (T3 0.0) (T4 0.0) )))
    # Example status 2: (DIF (NAME "Output Readings" (DATA (BULK 99.7) (CH1 10.123456 1.123000 1) (CH2 0.000000 0.000000 0) (T1 20.7) (T2 21.0) (T3 0.0) (T4 0.0) )))
    def ParseGetStatus(self, get_status_response):
        self.bulk_voltage = self.__parseBulkVoltage__(get_status_response)
        self.channel_data = self.__parseAllChannelData__(get_status_response)

        return self
    
    # e.g. parse "99.7" from (DIF (NAME "Output Readings" (DATA (BULK 99.7) (CH1 10.123456 1.123000 1) (T1 20.7) (T2 0.0) (T3 0.0) (T4 0.0) )))
    def __parseBulkVoltage__(self, get_status_response):
        try:
            bulk_voltage = None
            # find start of BULK in get status response
            bulk_start_index = get_status_response.find(b"BULK ")

            # find first ) after BULK, extract bulk voltage string, and confirm float bulk voltage
            if bulk_start_index > -1: 
                bulk_parenthesis_end_index = get_status_response.find(b")", bulk_start_index)
                bulk_voltage_str = get_status_response[bulk_start_index + 5 : bulk_parenthesis_end_index]

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
    
    
    #(CH1 10.123456 1.123000 1)
    def __parseAllChannelData__(self, get_status_response):
        try:
            channel_data_list = []
            channel_data_found = True
            last_channel_data_start_index = 0

            while channel_data_found == True:
                search_str = b"CH"
                channel_data_start_index = get_status_response.find(search_str, last_channel_data_start_index)

                if channel_data_start_index != -1:
                    channel_data_end_index = get_status_response.find(b")", channel_data_start_index)
                    channel_data_str = get_status_response[channel_data_start_index - 1:channel_data_end_index + 1]
                    channel_data = ChannelData.ChannelData().ParseChannelData(channel_data_str)
                    channel_data_list.append(channel_data)
                    last_channel_data_start_index = channel_data_start_index + len(search_str)
                else:
                    channel_data_found = False

            return channel_data_list
        except Exception as err:
            # print any error to terminal and raise to function caller
            print("Error parsing channel status: {}".format(err))
            raise

    def __parseAllTemperatureData__(self, get_status_response):
        try:
            temperature_status = []
            return temperature_status
        except Exception as err:
            # print any error to terminal and raise to function caller
            print("Error parsing temperature status: {}".format(err))
            raise   