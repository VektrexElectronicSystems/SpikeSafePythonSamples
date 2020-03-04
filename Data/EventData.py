# Goal: Parse SpikeSafe events into an accessible object
# Example event 1: 102, External Paused Signal Stopped
# Example event 2: 200, Max Compliance Voltage; Channel(s) 1,2,3

import math

class EventData():
    
    event = None

    code = 0

    message = None

    channel_list = []

    def __init__(self):
        pass
        
    # Goal: Helper function to parse event_data from SpikeSafe
    def ParseEventData(self, event_data):
        try:
            # populate object with extracted values
            self.event = event_data
            self.code = self.__parseEventCode__(event_data)                                     
            self.message = self.__parseEventMessage__(event_data)                               
            self.channel_list = self.__parseEventChannelList__(event_data)
            
            # return event data object to caller
            return self                                                             
        except Exception as err:
            # print any error to terminal and raise error to function caller
            print("Error parsing event data: {}".format(err))                             
            raise                                                               

    #Goal: Helper function parse event_data code from SpikeSafe message
    # e.g. parse "200" from "200, Max Compliance Voltage; Channel(s) 1,2,3"
    def __parseEventCode__(self, event_data):
        try:
            code = None
            # split event data by ",". e.g. [200, Max Compliance Voltage; Channel(s) 1,2,3]                                                                                                                                                    
            event_data_arr = event_data.split(b',', 1)                                      
            # set integer code
            code = int(event_data_arr[0])                                                   

            # return code to caller
            return code
        except Exception as err:
            # print any error to terminal and raise error to function caller
            print("Error parsing event code: {}".format(err))                                   
            raise                                                                                

    #Goal: Helper function parse event_data message from SpikeSafe message data
    # e.g. parse "Max Compliance Voltage" from "200, Max Compliance Voltage; Channel(s) 1,2,3"
    def __parseEventMessage__(self, event_data):
        try:
            message = None
            # split event data by ",". e.g. [200, Max Compliance Voltage; Channel(s) 1,2,3]                                                                      
            event_data_arr = event_data.split(b',', 1)
            # split second section by ";". e.g. [ Max Compliance Voltage, Channel(s) 1,2,3]
            event_message_arr = event_data_arr[1].split(b';')                               
            # remove all whitespace set message to value. e.g. Max Compliance Voltage
            message = event_message_arr[0].strip()                                      

            # return message to caller    
            return message                                                                      
        except Exception as err:
            # print any error to terminal & raise error to function caller
            print("Error parsing event message: {}".format(err))                                
            raise                                                                               

    #Goal: Helper function parse "Channel(s) 1,2,3" from "200, Max Compliance Voltage; Channel(s) 1,2,3"
    # note. Channel list is an optional section of the event data
    def __parseEventChannelList__(self, event_data):
        try:
            # channel list to return to caller
            channel_list = []
            # find start of Channel(s) in event data. e.g. [200, Max Compliance Voltage; |C|hannel(s) 1,2,3]
            channels_index = event_data.find(b"Channel(s)")         

            # ensure Channel(s) was found
            if channels_index > -1:
                # grab the substring of just the channels. e.g. [1,2,3]
                channel_list_str = event_data[channels_index + 11:] 
                # split channel substring by ",". e.g. [1,2,3]
                channel_list_str_arr = channel_list_str.split(b',')     

                # store all channels as integers in channel list
                for channel_str in channel_list_str_arr:                
                    channel_list.append(int(channel_str))

            # return channel list to caller
            return channel_list                                         
        except Exception as err:
            # print any error to terminal and raise error to function caller
            print("Error parsing event channel list: {}".format(err))   
            raise                                                     