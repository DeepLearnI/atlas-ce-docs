<h1>Log metrics</h1>
<span style="float:right;">[[source]](https://github.com/DeepLearnI/foundations/blob/master/foundations/stage_logging.py#L13)</span>

### log_metric


```python
log_metric(key, value)
```



Log a metric with Foundation when it is called. After job is finished, metric is accessible programmatically or through GUI.

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
from algorithms import calculate_score

def my_function(self):
    score = calculate_score()
    foundations.log_metric('score', score)
    return score

print(my_function)
```


