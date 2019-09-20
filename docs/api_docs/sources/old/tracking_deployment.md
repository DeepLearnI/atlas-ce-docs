<h1>Tracking a deployment</h1>
The following methods are members of the deployment object returned when the **deploy()** functions to trigger a new job is called.

----

<span style="float:right;">[[source]](https://github.com/DeepLearnI/foundations/blob/master/foundations/deployment_wrapper.py#L21)</span>

### job_name


```python
job_name(self)
```



Gets the name of the job being run.

__Arguments__

- This method doesn't receive any arguments.

__Returns__

- __job_name__ (string): The name of the job being run.

__Raises__

- This method doesn't raise any exception.

__Example__

```python
import foundations

deployment = foundations.deploy(job_directory=src, entrypoint=main.py, env=aws)
job_name = deployment.job_name()
print('Running job:', job_name)
```


----

<span style="float:right;">[[source]](https://github.com/DeepLearnI/foundations/blob/master/foundations/deployment_wrapper.py#L46)</span>

### is_job_complete


```python
is_job_complete(self)
```



Returns whether the job being run has completed.

__Arguments__

- This method doesn't receive any arguments.

__Returns__

- __is_job_complete__ (boolean): True if the job is done, False otherwise (regardless of success / failure).

__Raises__

- This method doesn't raise any exception.

__Example__

```python
import foundations

deployment = foundations.deploy(job_directory=src, entrypoint=main.py, env=gcp)
if deployment.is_job_complete():
	print('Job has finished.')
else:
	print('Job is still running.')
```


----

<span style="float:right;">[[source]](https://github.com/DeepLearnI/foundations/blob/master/foundations/deployment_wrapper.py#L142)</span>

### wait_for_deployment_to_complete


```python
wait_for_deployment_to_complete(self, wait_seconds=5)
```



Waits for the job to complete. It checks the status of the job periodically to test for completion.

__Arguments__

- __wait_seconds__ (float): The number of seconds to wait between job status check attempts (defaults to 5).

__Returns__

- This method doesn't return a value.

__Raises__

- This method doesn't raise any exception.

__Notes__

A job is completed when it finishes running due to success or failure. This method will wait for
any of these events to occur.

__Example__

```python
import foundations

deployment = foundations.deploy(job_directory=src, entrypoint=main.py, env=gcp)
deployment.wait_for_deployment_to_complete(wait_seconds=3)
print('Job has finished.')
```


----

<span style="float:right;">[[source]](https://github.com/DeepLearnI/foundations/blob/master/foundations/deployment_wrapper.py#L180)</span>

### get_job_status


```python
get_job_status(self)
```



Similar to is_job_complete, but with more information.

__Arguments__

- This method doesn't receive any arguments.

__Returns__

- __status__ (string): String, which is either "Queued", "Running", "Completed", or "Error".

__Raises__

- This method doesn't raise any exception.

__Example__

```python
import foundations

deployment = foundations.deploy(job_directory=src, entrypoint=main.py, env=gcp)

status = deployment.get_job_status()
print('Current job status:', status)
```


----

<span style="float:right;">[[source]](https://github.com/DeepLearnI/foundations/blob/master/foundations/deployment_wrapper.py#L206)</span>

### get_job_logs


```python
get_job_logs(self)
```



Get logs for job deployed with remote job deployment. Will return a "snapshot" of the logs at the moment of execution.

__Arguments__

- This method doesn't receive any arguments.

__Returns__

- __log__ (string): String, which is the contents of the log stream.

__Raises__

- This method doesn't raise any exception.

__Example__

```python
import foundations
import time

deployment = foundations.deploy(job_directory=src, entrypoint=main.py, env=gcp)

while not deployment.is_job_complete():
	try:
	    print(deployment.get_job_logs())
	except:
	    print("No logs generated yet")
	time.sleep(3)
```


