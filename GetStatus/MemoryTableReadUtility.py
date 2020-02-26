# Goal: Parse SpikeSafe get status into an accessible object
# Example status 1: (DIF (NAME "Output Readings" (DATA (BULK 99.7) (CH1 10.123456 1.123000 1) (T1 20.7) (T2 0.0) (T3 0.0) (T4 0.0) )))
# Example status 2: (DIF (NAME "Output Readings" (DATA (BULK 99.7) (CH1 10.123456 1.123000 1) (CH2 0.000000 0.000000 0) (T1 20.7) (T2 21.0) (T3 0.0) (T4 0.0) )))

from GetStatus import ChannelData
from GetStatus import MemoryTableRead
from GetStatus import TemperatureData

def ParseMemoryTableRead(get_status_response):
    memory_table_read = MemoryTableRead.MemoryTableRead()                       # get status object to return
    memory_table_read.bulk_voltage = __parseBulkVoltage__(get_status_response)  # extract bulk voltage from SpikeSafe get status response

    return memory_table_read

# e.g. parse "99.7" from (DIF (NAME "Output Readings" (DATA (BULK 99.7) (CH1 10.123456 1.123000 1) (T1 20.7) (T2 0.0) (T3 0.0) (T4 0.0) )))
def __parseBulkVoltage__(get_status_response):
    try:
        bulk_voltage = None                                                                             # bulk voltage to return to caller
        bulk_start_index = get_status_response.find(b"BULK ")                                           # find start of BULK in get status response

        if bulk_start_index > -1: # ensure BULK was found
            bulk_parenthesis_end_index = get_status_response.find(b")", bulk_start_index)               # find first ) after BULK
            bulk_voltage_str = get_status_response[bulk_start_index + 5 : bulk_parenthesis_end_index]   # extract bulk voltage string

            if isinstance(float(bulk_voltage_str), float) == True:                                      # ensure bulk voltage string is a float
                bulk_voltage = float(bulk_voltage_str)                                                  # set bulk voltage as a float                                                   

        if bulk_voltage == None:                                                                        # unexpected bulk voltage detected from SpikeSafe, end parsing
            raise Exception('Could not parse bulk voltage from: {}'.format(get_status_response))

        return bulk_voltage                                                                             # return bulk voltage to caller

    except Exception as err:
        print("Error parsing bulk voltage: {}".format(err))                                             # print any error to terminal
        raise                                                                                           # raise error to function caller

def __parseChannelStatus__(get_status_response):
    try:
        channel_status = []
        return channel_status
    except Exception as err:
        print("Error parsing channel status: {}".format(err))                                           # print any error to terminal
        raise                                                                                           # raise error to function caller

def __parsetemperatureStatus__(get_status_response):
    try:
        temperature_status = []
        return temperature_status
    except Exception as err:
        print("Error parsing temperature status: {}".format(err))                                           # print any error to terminal
        raise                                                                                           # raise error to function caller


