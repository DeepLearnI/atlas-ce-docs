<h1>Allocating Resource for Deployments</h1>
The following method is used to specify infrastructure resources for running jobs, if desired. Users should be able to specify the amount of GPUs and RAM they'd like the job to use, in order to speed up or prioritize jobs.

---
<span style="float:right;">[[source]](https://github.com/DeepLearnI/foundations/blob/master/foundations_contrib/set_job_resources.py#L11)</span>

### set_job_resources


```python
set_job_resources(num_gpus=1, ram=None)
```



Specifies the resources to run a job with. The available amount will greatly depend on what is available on the infrastrcture that the Foundations job orchestrator is setup on.

__Arguments__

- __num_gpus__ (int): The number of GPUs to run the job with.  Set to 0 to run with CPU resources instead.  By default uses 1 GPU.
- __ram__ (number): The maximum amount of ram in GB to use while running the job. Must be greater than 0 or None.  If None, no limit will be set.

__Returns__

- This function doesn't return a value.

__Raises__

ValueError: If either the RAM or GPU quantity is an invalid value (ex: less than 0) or not specified.

__Notes__

Setting the resources for a job from a given notebook or driver file will cause any additional jobs (ex: hyperparameter search) deployed from the same file and using the same process to use the same resources, unless specified otherwise.
To clear specifying resources and use the default, you can pass in set_job_resources(1, None).  Set num_gpus=0 to use CPU instead.

__Example__

```python
import foundations

#Deploys a job to use 2 GPUs and 4 Gb of RAM
foundations.set_job_resources(2, 4)
foundations.deploy(job_directory=src, entrypoint=main.py, env=aws)
```



