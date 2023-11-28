# [spikesafe-python API Overview](/spikesafe_python_lib_docs/README.md) | [Compensation](/spikesafe_python_lib_docs/Compensation/README.md) | get_optimum_compensation(spikesafe_model_max_current_amps, set_current_amps)

## get_optimum_compensation(spikesafe_model_max_current_amps, set_current_amps)

### Definition
Returns the optimum compensation for a given set current.

### Parameters
spikesafe_model_max_current_amps [float](https://docs.python.org/3/library/functions.html#float)  
Maximum current of the SpikeSafe model

set_current_amps [float](https://docs.python.org/3/library/functions.html#float)  
Current to be set on SpikeSafe

### Returns
[int](https://docs.python.org/3/library/functions.html#int)  
Load impedance command argument with optimum compensation

[int](https://docs.python.org/3/library/functions.html#int)  
Rise time command argument with optimum compensation

### Raises
[ValueError](https://docs.python.org/3/library/exceptions.html#ValueError)  
If set_current_amps is greater than spikesafe_model_max_current_amps