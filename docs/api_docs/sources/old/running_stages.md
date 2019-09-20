<h1>Running stages</h1>
After calling **create_stage()**, a callable object &mdash; with the same arguments as the wrapped function &mdash; is returned. When this object is called &mdash; in the same way as the wrapped function would be called &mdash; the user receives a stage object as a result that can be passed further. The following methods are members of this stage object.
<a id="hyperparameter_example"></a>

----

<span style="float:right;">[[source]](https://github.com/DeepLearnI/foundations/blob/master/foundations/stage_connector_wrapper.py#L95)</span>

### run


```python
run(self, params_dict=None, job_name=None)
```



Deploys and runs the current stage and the stages on which it depends in the configured execution
environment, creating a new job.

__Arguments__

- __job_name__ (string): optional name for the job that would be created.
- __params_dict__ (dict): optional way to pass values to stages that receive Foundation's Hyperparameter object(s).

__Returns__

- __deployment__ (DeploymentWrapper): An object that allows tracking the deployment.

__Raises__

- __    TypeError__: When the type of an argument passed to the function wrapped by this stage is not supported.

__Notes__

The new job runs asynchronously, the current process can continue execution.

You can pass hyperparameters values using both *params_dict* or keyword arguments syntax.

__Example__

```python
import foundations
from algorithms import train_model

train_model = foundations.create_stage(train_model)
model = train_model(data1=foundations.Hyperparameter(), data2=foundations.Hyperparameter())
model.run(job_name='Experiment number 2', params_dict={'data1': 'value1'}, data2='value2')
```


----

<span style="float:right;">[[source]](https://github.com/DeepLearnI/foundations/blob/master/foundations/stage_connector_wrapper.py#L57)</span>

### enable_caching


```python
enable_caching(self)
```



Activates caching of the result of current stage and any other stages that it depends on.

__Arguments__

- This method doesn't receive any arguments.

__Returns__

- __    stage object__: The same object to which this method belongs.

__Raises__

- This method doesn't raise exceptions.

__Example__

```python
import foundations
from data_helper import load_data
from algorithms import train_model

load_data = foundations.create_stage(load_data)
train_model = foundations.create_stage(train_model)
data = load_data()
model = train_model(data)
model.enable_caching()
model.run()
```


----

<span style="float:right;">[[source]](https://github.com/DeepLearnI/foundations/blob/master/foundations/stage_connector_wrapper.py#L170)</span>

### split


```python
split(self, num_children)
```



When a function is wrapped in a stage and it has more than one return value (the return value
is a sequence), the wrapping stage cannot obtain how many values are contained in the returned
sequence due to language constraints. This method allows to specify the number of children values
and splits the result in a corresponding sequence of stages that can be passed forward.

__Arguments__

- __num_children__ (int): number of children values contained in the stage result.

__Returns__

- __children_stages__ (sequence): A sequence of children stages.

__Raises__

- __    TypeError__: If the current stage does not contain a sequence of values.
- __    IndexError__: If the number of children values is less than __num_children__.

__Notes__

The exceptions thrown by this method only occur after the wrapped function is executed inside the
stage, when Foundations applies the splitting logic to the results. As a consequence,
these exceptions are thrown at a later time, when the stage is being executed in a job.

__Example__

```python
import foundations
from algorithms import retrieve_latitude, retrieve_longitude, train_with_coordinates

def get_coordinates():
	x_coord = retrieve_longitude()
	y_coord = retrieve_latitude()
	return x_coord, y_coord

get_coordinates = foundations.create_stage(get_coordinates)
train_with_coordinates = foundations.create_stage(train_with_coordinates)
x_coord, y_coord = get_coordinates().split(2)
model = train_with_coordinates(x_coord, y_coord)
model.run()
```


