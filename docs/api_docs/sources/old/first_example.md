<h1>Getting Started with Foundations</h1>

In this tutorial we will go over how to deploy and track a model using Foundations, as well as demonstrate additional features. To use Foundations to its maximum extent, we recommend seperating any job deployment code from the actual model itself. For this example, we will seperate all model code into a file called model.py and any job deployment code into deploy.py which will just use the functions defined in model.py. 

This tutorial showcases how you can use Foundations end-to-end to:  

  - Train a simple neural net on the famous MNIST dataset
  - Tune the model across multiple parameters to optimize accuracy
  - Bundle the code into a reuseable model package format
  - Deploy the model and run predictions

<h3>Before you start</h3>

You should have already [installed Foundations](../quick_start/). Some additional python dependencies you will need include: `keras`, `tensorflow`.  

## Set your configuration (optional)
This tutorial will deploy and run model code on your local machine using the auto-generated environment configuration file from the [init](../foundations_cli/#project-creation) command. However, if you are:

 - Planning on running your foundations code on a remote environment like Google Cloud Platform (GCP) or SSH
 - Want to modify where foundations stores data when running locally
 - Want to setup a cache
 - Looking to modify the verbosity of foundations logs
 - Looking to set environment variables in your deployment environment

you can customize your configurations. Instructions and examples on how to do this can be found [here](../configs/#configuration-options). 

Additional information on what deployment environments are and how to set up Foundations configuration files can be found under [Deploying to Different Environments](../configs/)

*By default, foundations will deploy locally, running your code on your local machine.*

## Create a new Foundations Project

We recommend that you create projects according to the Foundations default project template, which comes with a default folder structure for storing datasets, configuration and source code. Projects can automatically be created interactively using the Foundation CLI tool:

```
foundations init <project_name>
```

For this tutorial, lets create a project called `mnist_project`:
```
foundations init mnist_project
```
This should create a project directory as follows:
```
mnist_project                                    # Parent directory of the template
├── data                                         # Local project data
├── experiments                                  # Project experiments
│   └── mnist_project                            # Individual project experiments
│       ├── config                               # Experiment configuration files
│       │   ├── requirements.txt                 # Python dependencies  the experiment
│       │   ├── foundations_job_parameters.json  # Parameters to run experiments with 
│       │   └── local.config.yaml                # Local Foundations config
│       ├── src                                  # Experiment source code
│       └── artifacts                            # Foundations job output artifacts
├── experiment_management                        # Code on how to deploy experiments
├── scripts                                      # Project related testing scripts
├── .gitignore                                   # Prevent staging of unnecessary files to git
└── README.md                                    # Project README
```

## Deploy model code as a Foundations job

Now that we've created our project structure, lets train a model! In the project directory, navigate to `experiments/mnist_project/src`, which is where we will be putting all the source code for our experiment. Let's create a `main.py` file (which will call our model functions and create a pipeline) as well as a `model.py` file (which will contain our model code):  

**main.py**
```python
"""
Call functions from our model file to create a pipeline which the model will execute
"""
from model import load_data, preprocess_data, build_model, train_model, eval_model

#Define Hyperparameters for training different models
num_classes = 10
batch_size = 128
epoch = 5

# 1. Load data
X_train, X_test, y_train, y_test = load_data()

# 2. Process data
X_train, X_test, Y_train, Y_test = preprocess_data(X_train, X_test, y_train, y_test, num_classes)

# 3. Build the neural net 
model = build_model()

# 4.a Train the model
trained_model = train_model(batch_size, epoch, model, X_train, X_test, Y_train, Y_test)

# 4.b Validate the model
eval_model(trained_model, X_test, Y_test)
```
**model.py**
```python
"""
Each function here can be considered as a step towards building a model. We break each step into individual functions
to make it easier to read and keep track of functionality.
"""
import numpy as np

from keras.datasets import mnist
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.utils import np_utils

def load_data():
    (X_train, y_train), (X_test, y_test) = mnist.load_data()
    return X_train, X_test, y_train, y_test

def preprocess_data(X_train, X_test, y_train, y_test, num_classes):
    X_train = X_train.reshape(60000, 784)
    X_test = X_test.reshape(10000, 784)
    X_train = X_train.astype('float32')
    X_test = X_test.astype('float32')
    X_train /= 255
    X_test /= 255
    Y_train = np_utils.to_categorical(y_train, num_classes)
    Y_test = np_utils.to_categorical(y_test, num_classes)
    return X_train, X_test, Y_train, Y_test

def build_model():
    model = Sequential()
    model.add(Dense(512, input_shape=(784,)))
    model.add(Activation('relu'))
    model.add(Dropout(0.2))
    model.add(Dense(512))
    model.add(Activation('relu'))
    model.add(Dropout(0.2))
    model.add(Dense(10))
    model.add(Activation('softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

def train_model(batch_size, epoch, model, X_train, X_test, Y_train, Y_test):
    result = model.fit(X_train, Y_train,
              batch_size=batch_size, nb_epoch=epoch, verbose=1,
              validation_data=(X_test, Y_test))
    return model

def eval_model(model, X_test, Y_test):
    score = model.evaluate(X_test, Y_test, verbose=1)
    print('Test score: '+ str(score[0]))
    print('Test accuracy: '+ str(score[1]))
```

Notice how right now the code has no Foundations functionality added to it. This is because Foundations can launch any python code you've written as a job, making it very simple to get experimenting with Foundations. You could run the code simply with `python main.py`, but lets try deploying this as a Foundations job!

In the project root directory, run the following:

```bash
$ foundations deploy --job-directory=experiments/mnist_project --entrypoint=src/main.py --project-name=mnist_project
```

Additional information on the `foundations deploy` command can be found under the [CLI documentation](../foundations_cli/)

If sucessfully deployed, Foundations will run the job on your local machine. You can see from the output that the model ran 5 iterations with a batch size of 1028 samples, giving us a final accuracy of 97.88%!
```
Train on 60000 samples, validate on 10000 samples
Epoch 1/5
2019-03-18 13:03:41.023255: I tensorflow/core/platform/cpu_feature_guard.cc:141] Your CPU supports instructions that this TensorFlow binary was not compiled to use: AVX2 FMA
60000/60000 [==============================] - 6s 92us/step - loss: 0.2520 - acc: 0.9244 - val_loss: 0.1162 - val_acc: 0.9639
Epoch 2/5
60000/60000 [==============================] - 5s 90us/step - loss: 0.0998 - acc: 0.9688 - val_loss: 0.0836 - val_acc: 0.9735
Epoch 3/5
60000/60000 [==============================] - 12s 208us/step - loss: 0.0730 - acc: 0.9773 - val_loss: 0.0777 - val_acc: 0.9757
Epoch 4/5
60000/60000 [==============================] - 9s 153us/step - loss: 0.0570 - acc: 0.9819 - val_loss: 0.0729 - val_acc: 0.9781
Epoch 5/5
60000/60000 [==============================] - 7s 110us/step - loss: 0.0457 - acc: 0.9851 - val_loss: 0.0653 - val_acc: 0.9788
10000/10000 [==============================] - 1s 57us/step
Test score: 0.06534448580869356
Test accuracy: 0.9788
```

## Track metrics and results with Foundations

Now that we've successfully deployed a job with Foundations, lets log some key metrics in order to better manage our experiments. We will add in `foundations.log_metric` to track the final score and accuracy of the model.

In our `model.py` file, add `import foundations` at the top of the file, as well as the following lines to our `eval_model` function:

```python
def eval_model(model, X_test, Y_test):
    score = model.evaluate(X_test, Y_test, verbose=1)
    print('Test score: '+ score[0])
    print('Test accuracy: '+ score[1])
    foundations.log_metric('Test score:', score[0])
    foundations.log_metric('Test accuracy:', score[1])
```

By simply adding these two lines of code, Foundations now can track the final test score and accuracy across any future jobs you deploy, easily accessible through the GUI.

Let's deploy the job again with: 

```bash
$ foundations deploy --job-directory=experiments/mnist_project --entrypoint=src/main.py --project-name=mnist_project
```

Once completed, you should be able to navigate to `https://localhost:6443` to view our job results! In addition, we can also retrieve our metrics using get_metrics_for_all_jobs(project_name) in Foundations:
```
Start a python interpreter and run following commands:
import foundations
foundations.get_metrics_for_all_jobs("mnist_project")
```
This will read logged metrics for jobs ran under `mnist_project`. It returns a pandas data frame.

## Enable Caching on Functions

One of the feature Foundations provides is the ability to cache functions in your code, reducing the number of computations needed and therefore saving both time and resources. This is useful for running multiple experiments when input value of some functions
don't change among different runs, so their results are the same and don't require re-calculations.

Lets try adding it to our `build_model()` function as this code doesn't change between different jobs. To enable caching on a function with Foundations, simply add the decorator `@foundations.cache`:

```python
#In model.py

@foundations.cache
def build_model():
  ...
```

Now when we re-run the job, Foundations will use the same model object for future jobs. To understand how Foundations determines when caching should or should not be used during job execution, check out our [FAQs](../faqs/#how-does-caching-work-foundations-when-does-a-stage-get-resued)

## Deploying to Remote Environments (optional)

To run jobs on remote environments, you will need to use different configuration files and additional resources when deploying the job. This can be done via configuration file management.

In addition, you may need to set environment variables in your environment first before deploying the job. For example, to deploy on GCP, you will need a environment variable pointing to a JSON keyfile:
```
%env GOOGLE_APPLICATION_CREDENTIALS=/absolute/path/to/keyfile.json
```
For more information on deploying to remote environments, please refer to the documentation [here](../)