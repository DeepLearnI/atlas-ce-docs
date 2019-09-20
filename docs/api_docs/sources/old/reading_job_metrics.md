<h1>Reading job metrics</h1>
<span style="float:right;">[[source]](https://github.com/DeepLearnI/foundations/blob/master/foundations/projects.py#L40)</span>

### get_metrics_for_all_jobs


```python
get_metrics_for_all_jobs(project_name, include_input_params=False)
```



Returns metrics for all jobs for a given project.

__Arguments__

- __project_name__ (string): Name of the project to filter by.
- __include_input_params__ (boolean): Optional way to specify if metrics should include all model input metrics.

__Returns__

- __metrics__ (DataFrame): A Pandas DataFrame containing all of the results.

__Raises__

- __ValueError__: An exception indicating that the requested project does not exist.

__Example__

```python
import foundations

deployment = foundations.deploy(project_name='my_project', entrypoint=main.py)
deployment.wait_for_deployment_to_complete()

all_metrics = foundations.get_metrics_for_all_jobs('my_project')
print_metrics(all_metrics)
```


