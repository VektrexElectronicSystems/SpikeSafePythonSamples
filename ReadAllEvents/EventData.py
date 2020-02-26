import math

class EventData():
    
    event = None

    code = 0

    message = None

    channel_list = []

    def __init__(self):
        pass
        
    # Goal: Helper function to parse event_data from SpikeSafe response
    def ParseEventData(self, event_response):
        try:
            # populate object with extracted values
            self.event = event_response
            self.code = self.__parseEventCode__(event_response)                                     
            self.message = self.__parseEventMessage__(event_response)                               
            self.channel_list = self.__parseEventChannelList__(event_response)
            
            # return event data object to caller
            return self                                                             
        except Exception as err:
            # print any error to terminal and raise error to function caller
            print("Error parsing event data: {}".format(err))                             
            raise                                                               

    #Goal: Helper function parse event_data code from SpikeSafe message
    # e.g. parse "200" from "200, Max Compliance Voltage; Channel(s) 1,2,3"
    def __parseEventCode__(self, event_response):
        try:
            code = None
            # split event response by ",". e.g. [200, Max Compliance Voltage; Channel(s) 1,2,3]                                                                                                                                                    
            event_data_arr = event_response.split(b',', 1)                                      

            # check an event response was split, remove the white-space, and confirm integer code
            if (len(event_data_arr) > 0 and                                                     
            isinstance(int(event_data_arr[0].strip()), int) == True):                           
                code = int(event_data_arr[0])                                                   

            if code == None:  
                # unexpected code detected from SpikeSafe, end parsing
                raise Exception('Could not parse event code from: {}'.format(event_response))

            return code
        except Exception as err:
            # print any error to terminal and raise error to function caller
            print("Error parsing event code: {}".format(err))                                   
            raise                                                                                

    #Goal: Helper function parse event_data message from SpikeSafe message data
    # e.g. parse "Max Compliance Voltage" from "200, Max Compliance Voltage; Channel(s) 1,2,3"
    def __parseEventMessage__(self, event_response):
        try:
            message = None
            # split event response by ",". e.g. [200, Max Compliance Voltage; Channel(s) 1,2,3]                                                                      
            event_data_arr = event_response.split(b',', 1)                                      

            # check an event response was split to at least two sections
            if len(event_data_arr) > 1:
                # split second section by ";". e.g. [ Max Compliance Voltage, Channel(s) 1,2,3]
                event_message_arr = event_data_arr[1].split(b';')                               
                
                # check the second section was split to at least one section. e.g. [ Max Compliance Voltage, Channel(s) 1,2,3]
                if len(event_message_arr) > 0:
                    # remove all whitespace set message to value. e.g. Max Compliance Voltage
                    message = event_message_arr[0].strip()                                      

            # unexpected message detected from SpikeSafe, end parsing
            if message == None:                                                                 
                raise Exception('Could not parse message code from: {}'.format(event_response))

            # return message to caller    
            return message                                                                      
        except Exception as err:
            # print any error to terminal & raise error to function caller
            print("Error parsing event message: {}".format(err))                                
            raise                                                                               

    #Goal: Helper function parse "Channel(s) 1,2,3" from "200, Max Compliance Voltage; Channel(s) 1,2,3"
    # note. Channel list is an optional section of the event response
    def __parseEventChannelList__(self, event_response):
        try:
            # channel list to return to caller
            channel_list = []
            # find start of Channel(s) in event response. e.g. [200, Max Compliance Voltage; |C|hannel(s) 1,2,3]
            channels_index = event_response.find(b"Channel(s)")         

            # ensure Channel(s) was found
            if channels_index > -1:
                # grab the substring of just the channels. e.g. [1,2,3]
                channel_list_str = event_response[channels_index + 11:] 
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