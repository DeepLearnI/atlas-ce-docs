<h1>Specifying Project Names For Your Experiments</h1>
<span style="float:right;">[[source]](https://github.com/DeepLearnI/foundations/blob/master/foundations/projects.py#L9)</span>

### set_project_name


```python
set_project_name(project_name='default')
```



Sets the project a given job. This allows Foundations to know that multiple jobs belong to the same project. The project name is later used to retrieve metrics and analyze experiments.

__Arguments__

- __project_name__ (string): Optional name specifying which project the job is part of. If no project name is specified, the job will be deployed under the "default" project.

__Returns__

- This function doesn't return a value.

__Raises__

- This method doesn't raise any exceptions.

__Notes__

This function needs to be run before deploying a job using the Foundations SDK. If this is added in your deployment code, the project_name will not be updated.
For deployments using the CLI, there is an optional parameter to specify the project_name before deployment.

__Example__

```python
import foundations
from algorithms import train_model

foundations.set_project_name("my project")

foundations.deploy(env='local', entrypoint='main.py', job_directory='src')
```


