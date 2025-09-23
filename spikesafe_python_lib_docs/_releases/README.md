# spikesafe-python Releases

## v1.10.2
9/23/25

- Added
    - DigitizerDataFetch.fetch_voltage_data() new optional parameter digitizer_number
    - DigitizerDataFetch.fetch_voltage_data_sampling_mode_custom() new optional parameter digitizer_number
    - DigitizerDataFetch.fetch_voltage_data_sampling_mode_linear() new optional parameter digitizer_number
    - DigitizerDataFetch.fetch_voltage_data_sampling_mode_logarithmic() new optional parameter digitizer_number
    - DigitizerDataFetch.wait_for_new_voltage_data() new optional parameter digitizer_number

## v1.9.7
9/17/25

- Added
    - Support for package aggregation (single statement import spikesafe_python)
    - Support upload-artifact@v4 in .yml
    - Precision.get_precise_pulse_width_correction_command_argument
    - SerialPortConnection class
    - SpikeSafeEvents
        - INTERNAL_BULK_OVER_CURRENT = 209
        - MAXIMUM_BULK_VOLTAGE_BOOST_EXCEEDED = 210
        - PULSE_WIDTH_ADJUSTMENT_ERROR = 211
        - EXCESSIVE_BULK_VOLTAGE = 212
        - BULK_POWER_FAILURE = 213
        - INVALID_PARTIAL_ABORT = 434
        - CANNOT_COMMUNICATE_WITH_DIGITIZER = 510
        - INVALID_VOLTAGE_PROTECTION_MODE = 600
- Updated
    - Design for accessing static methods and enums by specifying class name, while supporting backwards compatibility
    - Compensation.get_custom_compensation() enable_logging default to False 
    - Compensation.get_optimum_compensation() enable_logging default to False
    - DigitizerDataFetch.wait_for_new_voltage_data() to check for VOLT:NDAT? PARTIAL
    - EventData.parse_event_data() to support events with physical channel list

## v1.8.3
1/23/25

- Added
    - jsonschema to requirements.txt
    - New info message "Custom compensation for {set_current_amps}A on {spikesafe_model_max_current_amps}A SpikeSafe model and device type '{device_type}' is LoadImpedance.{target_load_impedance} and RiseTime.{target_rise_time}." to Compensation.get_custom_compensation()
    - New parameter enable_logging to Compensation.get_custom_compensation()
    - New 80A SpikeSafe Model to Compensation.get_optimum_compensation()
    - Default return of LoadImpedance.MEDIUM and RiseTime.FAST if SpikeSafe Model isn't defined in Compensation.get_optimum_compensation()
    - New parameter enable_logging to Compensation.get_optimum_compensation()
    - New warning message "DC based modes do not require compensation, defaulting to LoadImpedance.VERY_LOW and RiseTime.VERY_SLOW" to Compensation.get_optimum_compensation()
    - New warning message "Compensation is intended for Pulse On Time of {optimum_compensation_minimum_pulse_on_time_seconds}s or less, defaulting to LoadImpedance.VERY_LOW and RiseTime.VERY_SLOW" to Compensation.get_optimum_compensation()
    - New warning message "{spikesafe_model_max_current_amps}A SpikeSafe Model not defined for optimum compensation, defaulting to LoadImpedance.MEDIUM and RiseTime.FAST" to Compensation.get_optimum_compensation()
    - New info message "Optimum compensation for {set_current_amps}A on {spikesafe_model_max_current_amps}A SpikeSafe model is LoadImpedance.{load_impedance} and RiseTime.{rise_time}." to Compensation.get_optimum_compensation()
    - New function ChannelData.current_reading_formatted_float()
    - New function ChannelData.current_reading_formatted_string()
    - New function ChannelData.voltage_reading_formatted_float()
    - New function ChannelData.voltage_reading_formatted_string()
    - New function DigitizerData.voltage_reading_formatted_float()
    - New function DigitizerData.voltage_reading_formatted_string()
    - New parameter enable_logging to DigitizerDataFetch.wait_for_new_voltage_data()
    - New function MemoryTableReadData.bulk_voltage_volts_formatted_float()
    - New function MemoryTableReadData.bulk_voltage_volts_formatted_string()
    - New class ScpitFormatter
    - New parameters enable_logging, default_log_level to TcpSocket()
    - pytests under tests/
        - test_optimum_compensation
- Fixed
    - Precision.get_precise_pulse_width_offset_command_argument()

## v1.7.17
10/25/24

- Added
    - Official support for Python 3.13
    - New function Compensation.get_custom_compensation()
    - New function Compensation.load_custom_compensation_table()
    - New function Compensation.load_custom_compensation_unique_device_types()
    - New schema Compensation.custom_compensation_table_schema
    - New attribute DigitizerData.time_since_start_seconds
    - New function DigitizerDataFetch.fetch_voltage_data_sampling_mode_linear()
    - New function DigitizerDataFetch.fetch_voltage_data_sampling_mode_logarithmic()
    - New function DigitizerDataFetch.fetch_voltage_data_sampling_mode_custom()
    - New enum DigitizerEnums.TimeSamplingMode
    - New enum DigitizerEnums.SamplingMode
    - New class DigitizerVfCustomSequence
    - New class DigitizerVfCustomSequenceStep
    - New class PulseWidthCorrection
    - New SpikeSafeEvents
        - MAX_COMPLIANCE_VOLTAGE_EXCEEDED_LIMIT = 125
        - INVALID_OFF_TIME_CAUSED_BY_INVALID_PULSE_WIDTH_CORRECTION = 395
        - INVALID_ON_TIME_CAUSED_BY_INVALID_PULSE_WIDTH_CORRECTION = 396
        - CHANNEL_IS_PULSING_CANNOT_CHANGE_SETTING = 397
        - COMMUNICATION_ERROR_DURING_IDN_QUERY_I2C_IS_RESET = 398
        - CPLD_VERSIONS_DO_NOT_MATCH = 399
        - DIGITIZER_THE_INPUT_RELAYS_OF_THE_DEVICE_IS_DISCONNECTED = 431
        - DIGITIZER_MISSING_OUTPUT_TRIGGER_EDGE_PARAMETER = 432
        - SAMPLING_CUSTOM_SEQUENCE_IS_NOT_SET = 433
        - INVALID_VOLTAGE_PROTECTION_MODE = 500
        - EXCEED_MAX_TOTAL_NUMBER_OF_STEPS_IN_SAMPLING_CUSTOM_SEQUENCE = 501
        - INVALID_SAMPLING_CUSTOM_SEQUENCE = 502
        - EXCEED_MAX_TOTAL_READ_COUNT_IN_SAMPLING_CUSTOM_SEQUENCE = 503
        - EXCEED_MAX_SAMPLING_CUSTOM_SEQUENCE_STRING_LENGTH = 504
        - EXCEED_MAX_TOTAL_SAMPLING_TIME_IN_SAMPLING_CUSTOM_SEQUENCE = 505
        - EXCEED_MAX_TOTAL_SAMPLING_CUSTOM_SEQUENCE_STRING_LENGTH = 506
        - PREVIOUS_SEQUENCE_HAVE_NOT_BEEN_CLEARED = 507
        - NO_SEQUENCE_HAVE_BEEN_SET = 508
        - EXCEED_MAX_SAMPLING_CUSTOM_SEQUENCE_APERTURE = 509
    - pytests under tests/
        - test_custom_compensation
        - test_digitizer_fetch_time_of_sampling
        - test_optimum_pulse_width_correction
    - workflows under .github/workflows/
        - deploy_development.yml. Runs pytests, increments version, builds, and pushes to Test PyPI on push to development branch
        - deploy_master.yml. Runs pytests, builds, and pushes to PyPI on push to master branch
- Fixed
    - Precision function comments to return strings which match function return type
- Updated
    - Compensation.get_optimum_compensation() error message to format: Measurement current {set_current_amps}A exceeds SpikeSafe model maximum current capability of {spikesafe_model_max_current_amps}A.

## v1.6.0
2/13/24

- Added
    - Threading.wait() optional os_timer_resolution_offset_time parameter
- Updated
    - README refers to SpikeSafePythonSamples for install and usage instructions
    - Compensation. get_optimum_compensation() returns LoadImpedance.Medium for 500mA in Low Current Range and operating under 70% ratio

## v1.5.15
12/26/23

- Added
    - New function Compensation.get_optimum_compensation()
    - New function DigitizerDataFetch. get_new_voltage_data_estimated_complete_time()
    - New function Discharge.get_spikesafe_channel_discharge_time()
    - New function Precision.get_precise_compliance_voltage_command_argument()
    - New function Precision.get_precise_voltage_protection_ramp_dv_command_argument()
    - New function Precision.get_precise_voltage_protection_ramp_dt_command_argument()
    - New function Precision.get_precise_pulse_width_offset_command_argument()
    - New function Precision.get_precise_duty_cycle_command_argument()
    - New function Precision.get_precise_time_command_argument()
    - New function Precision.get_precise_time_milliseconds_command_argument()
    - New function Precision.get_precise_time_microseconds_command_argument()
    - New function Precision.get_precise_current_command_argument()
    - New class LoadImpedance()
    - New class RiseTime()

## v1.4.5
4/28/23

- Updated
    - README.md replaced "SMU" with "PSMU"
    - Made threading.wait() more accurate with time.perf_counter

## v1.3.0
1/10/23

- Updated
    - Migrated to projectpy.toml to support Python v3.11.1. This package works with Python v3.10.0 and up.

## v1.2.3
9/15/22

- Added:
    - SpikeSafeEvents IntEnum class
    - Link to spikesafe-python API Overview in README
    - Optional parameter for SCPI Logging
- Updated:
    Class comments for better readability

## v1.1.0
6/4/20

Initial release