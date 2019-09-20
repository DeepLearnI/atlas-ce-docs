<h1>API Documentation</h1>

## Deploying code

There are 2 ways to deploy a job to Foundations: via the CLI, or with Python.

**CLI**

```bash
foundations deploy [--env ENV] [--job-directory JOB_DIRECTORY] [--entrypoint ENTRYPOINT] [--project-name PROJECT_NAME]
```

__Arguments__

- __--env__ is the environment that Atlas will use to submit your job to be run.

- __--entrypoint__ is an optional argument that specifies which Python file will run your code. Default is `main.py`.

- __--job-directory__ is an optional argument that specifies the directory of code that will be deployed to run. The default is the directory that the command is run from.

- __--project-name__ is an optional argument that specifies the name of the project that the code falls under. Default is the name of the directory that is deployed.


**Python**

```python
deploy(project_name=None, env='local', entrypoint='main.py', job_directory=None, params=None)
```

__Arguments__

- __project_name__ (str): Optional argument that specifies the name of the project that the code falls under. Default is the name of the directory that is deployed.

- __env__ (str): The environment that Atlas will use to deploy your job to be run. Default is local deployment.

- __entrypoint__ (str): Optional argument that specifies which Python file will run your code.

- __job_directory__ (str): Optional argument that specifies the directory of code that will be deployed to run. The default is the directory that the command is run from.

- __params__ (str): Optional argument to pass parameters into a deployed job. This dictionary will be stored as "foundations_job_parameters.json" in the launched job and can be accessed within the job code via `foundations.load_params()`

__Example__

```python
import foundations
foundations.deploy(
    project_name="text_generation_simple",
    env="scheduler",
    entrypoint="main.py",
    job_directory="experiments/text_generation_simple"
    params={ "learning_rate": 0.001 }
)
```


## Loading parameters

Loads job parameters from a file called foundations_job_parameters.json that must exist in the root of the project as a dictionary. This will also log all loaded parameters in the GUI by default.

For more information on the foundations_job_parameters.json file, see [(TODO)]()

**Python**

```python
load_parameters(log_parameters=True)
```

__Arguments__

- __log_parameters__ (bool): Optional way to specify whether or not to log all parameter values in the GUI and SDK for the job.

__Returns__

- __parameters__ (dict): A dictionary of all the user-defined parameters for the model, from foundations_job_parameters.json.

__Raises__

- __FileNotFoundError__: When the foundations_job_parameters.json file is not found in the deployment directory.

__Example__

```python
import foundations
params = foundations.load_parameters()
```


## Logging parameters

Log an individual input parameter with Foundation when it is called. After job is finished, parameter is accessible programmatically or through GUI. Can log
additional values to an already existing parameter.

**Python**

```python
log_param(key, value)
```

__Arguments__

- __key__ (str): The name of the input parameter. Can reuse already defined keys.

- __value__ (number, str, bool, array of [number|str|bool], array of array of [number|str|bool]): the value associated with the given input parameter.

__Returns__

- This function doesn't return a value.

__Notes__

If this function is called by code not deployed through Foundations, no metrics will be tracked.

__Example__

```python
import foundations
foundations.log_param("learning_rate", 0.001)
```


## Log metrics

Logs a metric with Foundation when it is called. Logged metrics are accessible programmatically or through GUI as soon as this line runs within your job.

```python
log_metric(key, value)
```

__Arguments__

- __key__ (str): the name of the output metric.

- __value__ (number, str, bool, array of [number|str|bool], array of array of [number|str|bool]): the value associated with the given output metric.

__Returns__

- This function doesn't return a value.

__Raises__

- __TypeError__: When a value of a non-supported type is provided as the metric value.

__Notes__

If this function is called by code not deployed through Foundations, no metrics will be tracked.

__Example__

```python
import foundations
foundations.log_metric("accuracy", 0.99)
```


## Model serving

Serving allows you to quickly setup a REST server around a model. Upon serving a model, the logs will be displayed such that the user can keep track of what is happening. 

You can use "Control+C" to escape out of the logs while the model is still being served.

For more information on model packages and manifest files, please see [(TODO)]().

```bash
foundations serve start <job_id>
```