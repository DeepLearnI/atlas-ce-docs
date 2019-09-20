<h1>Getting Started with Foundations</h1>

In this tutorial, we will go over how to build and deploy a model using Foundations, as well as demonstrate additional features. To use Foundations to its maximum extent, we recommend seperating any job deployment code from the actual model itself. For this example, we will seperate all model code into a file called model.py and any job deployment code into deploy.py which will just use the functions defined in model.py.

<h3>Before you start</h3>

You should have already [installed Foundations](../quick_start/).

## Step 0: Set your configuration (optional)
This tutorial will deploy and run model code on your local machine using the auto-generated environment configuration file from the [init](../foundations_cli/#project-creation) command. However, if you want to

 - runyour foundations code on a remote environment like Google Cloud Platform (GCP) or SSH,
 - modify where foundations stores data when running locally,
 - set up a cache,
 - modify the verbosity of foundations logs, or
 - set environment variables in your deployment environment,

you can customize your configurations. Instructions and examples on how to do this can be found [here](../configs/#configuration-options). 

Additional information on what deployment environments are and how to set up Foundations configuration files can be found under [Deploying to Different Environments](../configs/)

*By default, foundations will deploy locally, and your code will run on your local machine.*

## Step 1: Create a new Foundations Project

We recommend that you create projects according to the Foundations default project template, which comes with a default folder structure for storing datasets, configuration and source code. Projects can automatically be created interactively using the Foundation CLI tool:

```
foundations init <project_name>
```

For this tutorial, lets create a project called `my_first_project`:
```
foundations init my_first_project
```
This should create a project directory as follows:
```
my_first_project
├── config
│   └── local.config.yaml
├── data
├── post_processing
│   └── results.py
├── project_code
│   ├── driver.py
│   └── model.py
└── README.txt
```

You're ready to deploy your first job! Foundations' projects automatically come pre-populated with some very basic code which can be run to verify that everything is setup correctly. Let's navigate to the project root directory and deploy it with the following command: 
```
foundations deploy project_code/driver.py --env=local
```
This indicates to Foundations to run the `driver.py` file locally. Additional information on deploying Foundations jobs can be found [here](../foundations_cli/#deploying-jobs).

## Step 2: Writing model code

Now that we've deployed a very simple example, let's add a little more to our code. Navigate to the project directory, and in `project_code` you should find a `model.py` and `driver.py` file. Open the `model.py` file and follow the instructions below:

Replace the contents of the `model.py` file the following code:
```python
# Naive model code
# Each function here can be consider as a step (stage) towards building a model.
import foundations

def incr_by_10(x):
	return x + 10

def mult(x, y):
	output = x * y
	foundations.log_metric('output', output)	
	return output
```

Here we have a basic model which takes an input(x), increases it's value by 10 and then multiples it by some value (y) to output result (y * (x+10))

This model consists of two steps:  
1. To increase value by 10  
2. To multiply this increased value by a given number

In the end, this model outputs a multiplied value.

For best coding practices we recommend breaking down model code into different small functions(steps). Structuring code into functions makes for more maintainable and re-usable code in the long run.

## Step 3: Use Foundations to run model code

Now that we've defined some functions for our model, lets create our main execution pipeline. Open the `driver.py` file and let's add some code to call the functions we previously defined. 

```python
import foundations
from model import incr_by_10, mult

# input to model
x = 20

# build step1 of model
incr_value = incr_by_10(x)

# build step2 of model
result = mult(x, incr_value)

# run the model
print(result)
```

The code above takes in an input x and first adds 10 to it, then multiplies the value of x by that amount. Because Foundations is non-intrusive to how you want to write your model code, we can directly deploy this as a Foundations job with: 

```
foundations deploy project_code/driver.py --env=local
```

This command allows you to specify the python file you want to deploy as a Foundations job, and where you want the job to run. For more information on deploying jobs, you can reference the documentation [here](../foundations_cli/#deploying-jobs).

## Step 3: Specifying project names for your experiments

You've just run your first job! You should be able to view the job in the [Web GUI](../gui/) at `https://localhost:6443` under `default`.

You will probably be running multiple jobs to train a model. We recommend defining a project and storing all information about your jobs and results under one this project name space. You can do this by setting project names in your code.
For example, in `driver.py` file, add
```
foundations.set_project_name("demo_project")
```

Everytime, a new job is ran, all results and job information coming out of this job will be stored under project space "demo_project". Rerunning the job should now have a new project on the GUI under "demo_project"

## Step 4: Log metrics in your model stages

To log metrics (so that you can evaluate them later) in your job runs when you are training your model, you can use the `log_metric` function.
For example, in `model.py` file lets add the following lines in `mult(x, y)`:
```python
foundations.log_metric('x', x)
foundations.log_metric('y', y)
```

This will log value of x with key as `x` and y with key as `y` in Foundations backend.
These values of x and y will be available to read after jobs finish running.

## Step 5: Reading logged metrics

Now that you have logged some metrics during model training, you'll want to read them after all your jobs are finished so that you can analyse your metrics. You can get all these metrics using get_metrics_for_all_jobs(project_name) on foundations:
```
Start a python interpreter and run following commands:
import foundations
foundations.get_metrics_for_all_jobs("demo_project")
```
To run this is in Jupyter, you can create a new cell and directly run the line above. This will read logged metrics for jobs ran under project name `demo_project`. It returns a pandas data frame.

## Step 6: Use Foundations caching feature

Now that you know how to log and read metrics for each job, you will want to train best model possible. You will be running jobs (model code) with various different data inputs and parameters. In these numerous jobs many computations will be similar, so Foundations has a smart way of detecting these identical computations across all jobs and re-using the already computated step instead of re-computing everytime for every job. We call it caching.
You will have to tell Foundations which step might get recomputed. This can be done by using enable_caching() on `stage_object`.
For example, in `driver.py` file let's add:
```
# build step1 of model
incr_value = incr_by_10(x)
incr_value.enable_caching()
```
This will enable the caching feature on `incr_value` stage_object. For every job ran, the return value from `incr_value` will be cached in Foundations.
Therefore, if first job runs `incr_value(3)` then its return value of `13` will be cached in Foundations. When second job runs `incr_value(3)`, Foundations will directly use pre-computed cached value `13` instead of re-computing this step. You can imagine how powerful this feature can become in model training.

## Step 7: Tracking and Retriving Job Artifacts (optional)

Now, let's say that we want to store the values of our mult function in the `model.py` file to be later used for analysis. Users can define create and specify a path where Foundations will a track during the job run. When the job is completed, any artifacts generated into that path will be persisted and stored for analysis. 

First, in the `project_code` folder, lets create an empty folder called `storedFiles`. This is where we'll store any artifacts from our job, to be saved by Foundations. Our project directory should look something like this:
```
project_name
├── config
│   └── local.config.yaml
├── data
├── post_processing
│   └── results.py
├── project_code
│   ├── artifacts
│   ├── driver.py
│   └── model.py
└── README.txt
```

Next, we'll have to modify our `local.config.yaml` configuration file, located in the `config` directory of the project. By adding a relative `artifact_path`, Foundations will track that path when the job is running:

```yaml
job_deployment_env: local
results_config:
  artifact_path: artifacts
cache_config: {}
obfuscate_foundations: False
```

In our model code, let's store the values of x and y as a dataframe and serialize it for later analysis. We can do this by adding ```import pandas as pd``` to the top of the file, as well as the following lines of code in the `mult` function:
```python
df = pd.DataFrame([[x,y]],columns=['x','y'])
df.to_pickle("artifacts/variables.pkl")
```

Let's deploy the job (make sure you keep track of the job_id!) with:
```bash
$foundations deploy project_code/driver.py --env=local
```

Once the job has completed running, we should be able to see that our files were written to disk and saved in the archives directory. By default, this can be found at: `~/.foundations/job_data/archive`. If we look under `~/.foundations/job_data/archive/<JOB_ID>`, we should see an artifacts folder, containing our `variables.pkl`! Files can be retrieved also with the Foundations CLI command `foundations retrieve artifacts`. To retrieve our pkl file, run the following:
```bash
$foundations retrieve artifacts --env=local --job_id=<JOB_ID>
```

Now, you should see that our variables.pkl file was downloaded to the present directory.

## Step 8: Deploying to Remote Environments (optional)

To run jobs on remote environments, you will need to use different configuration files and additional resources when deploying the job. This can be done via configuration file management 

In addition, you may need to set environment variables in your notebook first before deploying the job. For example, to deploy on GCP, you will need a environment variable pointing to a JSON keyfile:

```bash
%env GOOGLE_APPLICATION_CREDENTIALS=/absolute/path/to/keyfile.json
```

For more information on deploying to remote environments, please refer to the documentation [here](../configs/)

## Step 9: Adding additional dependencies (optional)

Be aware that installing a package locally doesn't mean it will be in the execution environment. If you want to use an external python package, you'll need to create a `requirements.txt` wherever your model code exists with the dependencies explicitly stated. The requirements file will be in the root of the model code directory. 

Reference the main [start guide](../start_guide/) for a more detailed explanation.

## Complete Tutorial Code
```python
# driver.py
import foundations
from model import incr_by_10, mult

foundations.set_project_name("demo_project")

# input to model
x = 20

# build step1 of model
incr_value = incr_by_10(x)
incr_value.enable_caching()

# build step2 of model
result = mult(x, incr_value)

# run the model
result.run()
```
```python
# model.py
# Naive model code
# Each function here can be consider as a step (stage) towards building a model.
import foundations

def incr_by_10(x):
    return x + 10

def mult(x, y):
    foundations.log_metric('x', x)
    foundations.log_metric('y', y)
    output = x * y
    foundations.log_metric('output', output)    
    return output
```
