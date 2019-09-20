<h1>Setting Deployment Environment</h1>
<span style="float:right;">[[source]](https://github.com/DeepLearnI/foundations/blob/master/foundations/config.py#L8)</span>

### set_environment


```python
set_environment(environment_name)
```



Sets the deployment environment where the job is run or to specify which deployment environment to manage jobs/get results from. Equivalent to specifying --env when deploying through the Foundations CLI.

__Arguments__

- __environment_name__ (string): the name of the deployment environment. Available environments can be displayed with the Foundations CLI command 'foundations info --env'.

__Returns__

- This function doesn't return a value.

__Raises__

- __ValueError__: An exception indicating that the specified environment_name does not exist.

__Notes__

This function needs to be run before deploying a job using the Foundations SDK. For deployments using the CLI, there is an optional parameter to specify the environment before deployment.

__Example__

```python
import foundations
from algorithms import train_model

foundations.set_environment("gcp")

foundations.deploy(project_name='my_project', entrypoint='main.py', job_directory='src')
```


