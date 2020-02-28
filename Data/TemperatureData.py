# Goal: Parse temperature portion of SpikeSafe memory table read into an accessible object
# Example: (T1 20.7) (T2 21.0)

import math

class TemperatureData():
    
    heat_sink_number = 0

    temperature_reading = math.nan

    def __init__(self):
        pass

    # Goal: Helper function to parse temperature portion of SpikeSafe memory table read into an accessible object
    def ParseTemperatureData(self, temperature_memory_table_read_response):
        try:
            # find start of T, extract "1 20.7" to string, and separate by " " into list
            search_str = b"T"
            temperature_data_start_index = temperature_memory_table_read_response.find(search_str)
            temperature_parsable_format = temperature_memory_table_read_response[temperature_data_start_index + len(search_str) : len(temperature_memory_table_read_response) - 1]
            temperature_response_split = temperature_parsable_format.split(b' ')

            # set all values
            self.heat_sink_number = int(temperature_response_split[0])
            self.temperature_reading = float(temperature_response_split[1])

            # return temperature data object to caller
            return self
        except Exception as err:
            # print any error to terminal and raise to function caller
            print("Error parsing temperature data from SpikeSafe memory table read: {}".format(err))                                            
            raise  