from GetStatus import ChannelData
from GetStatus import MemoryTableRead
from GetStatus import TemperatureData

def ParseMemoryTableRead(memory_table_read_str):
    memory_table_read = MemoryTableRead.MemoryTableRead()
    memory_table_read.bulk_voltage = __parseBulkVoltage__(memory_table_read_str)
    return memory_table_read

def __parseBulkVoltage__(memory_table_read_str):
    # bulk_start_index = memory_table_read_str.find('BULK') + 4
    # bulk_voltage_str = memory_table_read_str.IndexOf(')', bulk_start_index)
    bulk_voltage = float(0)
    return bulk_voltage

"""     int PosBulk = reading.IndexOf("BULK") + 4;
                int ParenEnd = reading.IndexOf(")", PosBulk);
                string BulkVStr = reading.Substring(PosBulk + 1, ParenEnd - PosBulk - 1);
                BulkVoltage = decimal.Parse(BulkVStr, NumberStyles.Number, CultureInfo.InvariantCulture); """