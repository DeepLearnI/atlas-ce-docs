<h1>Foundations Model Serving </h1>

Foundations provides a standard format for packaging your machine learning code so that it can be productionized seamlessly. This *model package* format defines a convention that lets you save a model with minimal refactoring, only specifying your code paths which can be later be understood by downstream interfaces.

##Model Package

Each Foundations model package is a directory containing several files, together with a `manifest` file in the root directory that specifies multiple code path `entrypoints` the package exposes for production. When running experiments with Foundations, all of this is automatically stored between jobs and can easily be deployed as long as a `foundations_package_manifest.yaml` file is present. For example, if we deploy an experiment from the default Foundations project template, our model package could look something like this:

```
mnist_project 
├── config
│   ├── requirements.txt
│   └── foundations_job_parameters.json
├── src
│   ├── main.py
│   ├── model.py
│   └── preprocessing.py
├── artifacts
│   └── my_model.h5
└── foundations_package_manifest.yaml
```

In the example above, the mnist_project directory essentially becomes the model package - all references to parameters, different functions/modules, and even files in the code are all preserved so no refactoring is needed to generate this package.

##Defining a manifest file
The `foundations_package_manifest.yaml` file is a configuration which specifies the entrypoint and different routes a model package could have. If serving via a REST server and API, these entrypoints would essentially become the routes.  

In the configuration, you will need to define the `function` (the code path your route will execute when called), and the `module` (which module the function comes from) for each entrypoint.

<h4>Manifest Options</h4>

**entrypoints.predict**: specifies how the model package will run predictions (inference) when served.

**Example manifest:**

From the experiment directory above, if our predict function lives in the `main.py` file, we can define our `foundations_package_manifest.yaml` file as such:

```yaml
entrypoints:
    predict:
        module: "src.main"
        function: "predict"
```
**Note:** Once a manifest has been added to your root directory, you will need to launch a new Foundations job in order for Foundations to be able to directly serve it.

##Serving a Model Package

Model packages can be served into a production environment directly with Foundations. Using the CLI command:

```
$foundations serve start <job_id>
```
Foundations automatically retrieves the bundle associated with the `job_id` and wraps it in a REST API server, where requests can be made to the entrypoints, specified by the `foundations_package_manifest.yaml` file. The command will return a generated model name associated with the served package, used to uniquely identify the package and for production management.

To stop a model package from serving, type the following command:

```
$foundations serve stop <model_name>
```

