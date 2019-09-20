<h1>Hyperparameter Tuning With Foundations</h1>

Foundations makes it really easy to optimize your model by supporting multi-job execution, as well as allowing you to load parameter values during runtime. Furthermore, Foundations automatically tracks the parameter values between different jobs, making it easy to trace and recreate previous experiments.

###Specifying Parameter Values

The recommended way to specify your model parameters values is by using a separate dictionary file. This not only makes it easy to specify a lot of different parameter values in one centralized location, but also makes tracking easier when running multiple jobs. When using Foundations to create a new project, a `foundations_job_parameters.json` is automatically created for you to store/load your parameter values from. Using the file is not a *requirement* to deploy jobs, but is highly recommended.

**Example foundations_job_parameters.json file:**
```json
{
    "learning_rate": 0.001,
    "batch_size": 64,
    "drop_out_rate": 0.45,
    "layer_shapes": [128, 256, 192, 128],
    "early_stopping_rounds": 4,
    "early_stopping_tolerance": 0.01,
    "regularization_param": 0,
    "epochs": 40
}
```

###Loading in parameter values to your code

To load in the parameters you've specified into your experiment, add the following function anywhere in your code:

```python
foundations.load_parameters()
```

This function will automatically retrieve the values from the `foundations_job_parameters.json` when executed, allowing use of the parameter values in your code when needed. In addition, by using this function, Foundations will automatically track the parameter values for the job on the GUI and SDK for analysis later. For example:

```python
#Example main.py
import foundations

params = foundations.load_parameters()
...

train_model(params["learning_rate"], params["epochs"])
```

Check out our [SDK reference](../load_parameters/) for more information.

###Launching multiple jobs

Using `foundations.deploy()`, foundations provides the flexibility to write your own hyperparameter search code and launch multiple jobs with a variety of different parameters to optimize your model. The function takes in a dictionary of parameter values as well as launching a new Foundations job when called so that structure your search as long as you load in the parameters with `foundations.load_parameters`. We recommend placing all scripts and code used launch multiple jobs in the `experiment_management` folder. An example of a random hyperparameter search can be found below:

**Random Search Example:**
```python
import foundations

param_ranges = {
    "epochs": {
        "min": 5,
        "max": 40,
    },
    "layer_shapes": {
        "min": 256,
        "max": 768,
        "count_min": 1,
        "count_max": 3
    }
    "early_stopping_tolerance": 0.01,
    "batch_size": [64, 128, 1024]
}

for _ in range(5):
    params = some_random_parameter_generator(param_ranges)
    foundations.deploy(env="gcp", job_directory="/path/to/job/code", entrypoint="src/main.py", params=params)
```