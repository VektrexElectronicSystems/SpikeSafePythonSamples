# Goal: Read all Spikesafe events from event queue
# SCPI Command: *SYST:ERR?
# SpikeSafe events are parsed into EventData class
# Example event 1: 102, External Paused Signal Stopped
# Example event 2: 200, Max Compliance Voltage; Channel(s) 1,2,3

from Data.EventData import EventData

def ReadAllEvents(spikeSafeSocket):
    try:
        # event list to be returned to caller
        event_data_list = []

        # initialize flag to check if event queue is empty 
        is_event_queue_empty = False                                                                                                                      

        # run as long as there is an event in the SpikeSafe queue
        while is_event_queue_empty == False:
            # request SpikeSafe events and read data
            spikeSafeSocket.sendScpiCommand('SYST:ERR?')                                        
            event_response = spikeSafeSocket.readData()                                        

            if event_response != '':
                 # parse all valid event responses from SpikeSafe into event_data class                                                           
                event_data = EventData().ParseEventData(event_response)

                if event_data.code != 0:
                    # events with code greater than 0 are valid, add these to event data list
                    event_data_list.append(event_data)                                  
                else:
                    # Example message: 0, OK
                    # When "0,OK is read the SpikeSafe event queue is empty
                    is_event_queue_empty = True                                                 
            else:
                # unexpected response detected from SpikeSafe, end checking
                raise Exception('No event response from SpikeSafe: {}'.format(event_response))  

        # return event list to caller        
        return event_data_list                                                                  
    except Exception as err:
        # print any error to terminal and raise error to function caller
        print("Error emptying event queue: {}".format(err))                                     
        raise                                                                             

