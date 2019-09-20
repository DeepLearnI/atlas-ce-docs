<h1>Deploying Foundations Jobs</h1>
The following method is how to deploy foundations jobs with Foundations SDK

---
<span style="float:right;">[[source]](https://github.com/DeepLearnI/foundations/blob/master/foundations/deploy.py#L8)</span>

### deploy


```python
deploy(project_name=None, env='local', entrypoint='main.py', job_directory=None, params=None)
```



Bundles everything from the job_directory and launches a new Foundations job to the specified environment.

__Arguments__

- __project_name__ (str): Optional way to specify the name of the project your job will be saved under.
- __env__ (str): The Foundations environment where the job should be deployed to. Jobs will run locally be default.
- __entrypoint__ (str): Optional way to specify the entrypoint filename. main.py by default.
- __job_directory__ (str): Optional way to specify what directory to bundle and deploy with Foundations. Will use present working directory by default.
- __params__ (str): the file containing you job parameters when executing. Will read from "foundations_job_parameters.json" by default.

__Returns__

- __deployment__ (DeploymentWrapper): An object that allows tracking the deployment.

__Raises__

- This method doesn't raise any exceptions.

__Example__

```python
import foundations
from algorithms import calculate_score

foundations.set_environment('gcp')
foundations.set_project_name('xgboost_test')

foundations.deploy(entrypoint='src/main.py', job_directory='experiments')
```

