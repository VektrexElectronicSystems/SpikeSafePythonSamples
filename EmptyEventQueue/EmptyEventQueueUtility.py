from EmptyEventQueue import EventData

def EmptyEventQueue(spikeSafeSocket):
    spikeSafeSocket.sendScpiCommand('SYST:ERR?')
    data = spikeSafeSocket.readData()                    # read SpikeSafe status
    print(data)                                     # print SpikeSafe response to terminal
    event_data_list = []
    event_data_list.append(EventData.EventData(0,'test',[1,2]))    
    event_data_list.append(EventData.EventData(0,'test',[3,4]))
    return event_data_list