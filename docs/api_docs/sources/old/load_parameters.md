<h1>Load Job Parameters</h1>
<span style="float:right;">[[source]](https://github.com/DeepLearnI/foundations/blob/master/foundations/job_parameters.py#L8)</span>

### load_parameters


```python
load_parameters(log_parameters=True)
```



Loads job parameters from the foundations_job_parameters.json file as a dictionary, in order to pass in parameter values into the job. Will also log all loaded parameters in the GUI .

__Arguments__

- __log_parameters__ (bool): Optional way to specify whether or not to log all parameter values in the GUI and SDK for the job.

__Returns__

- __parameters__ (dict): A dictionary of all the user-defined parameters for the model, from foundations_job_parameters.json.

__Raises__

- __FileNotFoundError__: When the foundations_job_parameters.json file is not found in the deployment directory.

__Example__

```python
import foundations
from model import train_model

params = foundations.load_parameters()

def my_func(self):
    model = train_model(params["layers"])

my_func()
```


----

<span style="float:right;">[[source]](https://github.com/DeepLearnI/foundations/blob/master/foundations/job_parameters.py#L58)</span>

### log_param


```python
log_param(key, value)
```



Log an individual input parameter with Foundation when it is called. After job is finished, parameter is accessible programmatically or through GUI. Can log
additional values to an already existing parameter.

__Arguments__

- __key__ (str): The name of the input parameter. Can reuse already defined keys.
- __value__ (number, str, bool, array of [number|str|bool], array of array of [number|str|bool]): the value associated with the given input parameter.

__Returns__

- This function doesn't return a value.

__Raises__

- __TypeError__: When a value of a non-supported type is provided as the metric value.

__Example__

```python
import foundations
from model import train_model

#Foundations will not automatically track all input parameters when log_params=False
params = foundations.load_parameters(log_params=False)

def my_func(self):
    model = train_model(params["layers"])
    foundations.log_param("layers", params["layers"])

my_func()
```


