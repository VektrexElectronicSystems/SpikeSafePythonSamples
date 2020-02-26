# Goal: Empty Spikesafe event queue by reading all events
# SCPI Command: *SYST:ERR?
# Example message 1: 102, External Paused Signal Stopped
# Example message 2: 200, Max Compliance Voltage; Channel(s) 1,2,3

from EmptyEventQueue import EventData

def EmptyEventQueue(spikeSafeSocket):
    try:
        event_data_list = []                                                                    # event list to be returned to caller
        is_event_queue_empty = False                                                            # flag to check if event queue is empty                                                           

        while is_event_queue_empty == False:                                                    # run as long as there is an event
            spikeSafeSocket.sendScpiCommand('SYST:ERR?')                                        # request SpikeSafe event
            event_response = spikeSafeSocket.readData()                                         # read SpikeSafe event

            if event_response != '':                                                            # parse all valid event responses from SpikeSafe
                event_data = __parseEventData__(event_response)

                if event_data.code != 0:                                                        # events with code greater than 0 are valid, add these to event queue
                    event_data_list.append(event_data)                                  
                else:
                    is_event_queue_empty = True                                                 # "0, OK" is detected, flag event queue as empty
            else:
                raise Exception('No event response from SpikeSafe: {}'.format(event_response))  # unexpected response detected from SpikeSafe, end checking

        return event_data_list                                                                  # return event list to caller
    except Exception as err:
        print("Error emptying event queue: {}".format(err))                                     # print any error to terminal
        raise                                                                                   # raise error to function caller

def __parseEventData__(event_response):
    try:
        code = __parseEventCode__(event_response)                                     # extract code from SpikeSafe event response
        message = __parseEventMessage__(event_response)                               # extract message from SpikeSafe event response
        channel_list = __parseEventChannelList__(event_response)                      # extract channel list from SpikeSafe event response

        event_data = EventData.EventData(event_response, code, message, channel_list) # create event data object with extracted values
        return event_data                                                             # return event data object to caller
    except Exception as err:
        print("Error parsing event data: {}".format(err))                             # print any error to terminal
        raise                                                                         # raise error to function caller

# e.g. parse "200" from "200, Max Compliance Voltage; Channel(s) 1,2,3"
def __parseEventCode__(event_response):
    try:
        code = None                                                                         # code to return to caller                                                                             
        event_data_arr = event_response.split(b',', 1)                                      # split event response by ",". e.g. [200, Max Compliance Voltage; Channel(s) 1,2,3]

        if (len(event_data_arr) > 0 and                                                     # check an event response was split
        isinstance(int(event_data_arr[0].strip()), int) == True):                           # remove white-space and check this is an integer. e.g. 200
            code = int(event_data_arr[0])                                                   # set code to value. e.g. 200

        if code == None:                                                                    # unexpected code detected from SpikeSafe, end parsing
            raise Exception('Could not parse event code from: {}'.format(event_response))

        return code
    except Exception as err:
        print("Error parsing event code: {}".format(err))                                   # print any error to terminal
        raise                                                                               # raise error to function caller

# e.g. parse "Max Compliance Voltage" from "200, Max Compliance Voltage; Channel(s) 1,2,3"
def __parseEventMessage__(event_response):
    try:
        message = None                                                                      # message to return to caller
        event_data_arr = event_response.split(b',', 1)                                      # split event response by ",". e.g. [200, Max Compliance Voltage; Channel(s) 1,2,3]

        if len(event_data_arr) > 1:                                                         # check an event response was split to at least two sections
            event_message_arr = event_data_arr[1].split(b';')                               # split second section by ";". e.g. [ Max Compliance Voltage, Channel(s) 1,2,3]
            
            if len(event_message_arr) > 0:                                                  # check the second section was split to at least one section. e.g. [ Max Compliance Voltage, Channel(s) 1,2,3]
                message = event_message_arr[0].strip()                                      # remove all whitespace set message to value. e.g. Max Compliance Voltage

        if message == None:                                                                 # unexpected message detected from SpikeSafe, end parsing
            raise Exception('Could not parse message code from: {}'.format(event_response))

        return message                                                                      # return message to caller
    except Exception as err:
        print("Error parsing event message: {}".format(err))                                # print any error to terminal
        raise                                                                               # raise error to function caller

# e.g. parse "Channel(s) 1,2,3" from "200, Max Compliance Voltage; Channel(s) 1,2,3"
# note. Channel list is an optional section of the event response
def __parseEventChannelList__(event_response):
    try:
        channel_list = []                                           # channel list to return to caller
        channels_index = event_response.find(b"Channel(s)")         # find start of Channel(s) in event response. e.g. [200, Max Compliance Voltage; |C|hannel(s) 1,2,3]

        if channels_index > -1:                                     # ensure Channel(s) was found
            channel_list_str = event_response[channels_index + 11:] # grab the substring of just the channels. e.g. [1,2,3]
            channel_list_str_arr = channel_list_str.split(b',')     # split channel substring by ",". e.g. [1,2,3]

            for channel_str in channel_list_str_arr:                # store all channels as integers in channel list
                channel_list.append(int(channel_str))

        return channel_list                                         # return channel list to caller
    except Exception as err:
        print("Error parsing event channel list: {}".format(err))   # print any error to terminal
        raise                                                       # raise error to function caller
    
