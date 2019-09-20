<h1>Setting Up Different Deployment Environments in Foundations</h1>

Foundations uses a configuration-driven approach to deployment, and which configurations are selected when deploying a job determines where the execution environment (compute) will occur.

Configuration in Foundations is done through `config.yaml` files.

## Concepts and Vocabulary

It's important to understand the language used around deployment so that we can properly understand how models are run, and where.

**Entrypoint**: this your main execution file.   

**Execution Environment**: this is the infrastructure where models are actually computed (ie: where the actual jobs are run). This can be a variety of different locations such as local (where you run model code on your local machine), or on a remote server (Google Cloud Platform, Amazon Web Services, other SSH servers). See below for more details on Types of Deployments.

**Deployment Environment**: See *Execution Environment*

**Job**: this is the unit used to describe the package that is the model, source code, and metadata that gets sent to be computed.  

**Deployment**: the process of bundling, transferring and running (executing) a Foundations job on any environment.  

**Queuing System**: a way for multiple jobs to be sent to the execution environment, where they'll be put in line before they get run.  

## Types of Deployments

Foundations works with a few different types of deployment options:

**Local Deployment:** this will run directly on the machine where the `.yaml` file is. This deployment doesn't require a queuing system. There are two versions of this, `local.config.yaml` for running on Linux and OSX, and `local_windows.config.yaml` for running on Windows.

**Google Cloud Platform (GCP) Deployment:** for use with Google's cloud service. A queuing system is required for use of this deployment configuration. When using this method of deployment, remember to authenticate with your Google Cloud service. Instructions on how to do this can be found [here](https://google-cloud.readthedocs.io/en/latest/core/auth.html).

**Amazon Web Services (AWS) Deployment:** for use with Amazon's cloud service. A queuing system is required for use of this deployment configuration. When using this method of deployment, remember to authenticate with your AWS service. Instructions on how to do this can be found [here](https://docs.aws.amazon.com/codedeploy/latest/userguide/auth-and-access-control.html).

**SSH Deployment:** this type of deployment uses a simple way of sending a job to a compute box and getting results. It expects to work with Foundations' SCP-style queueing system. 

To select which of the above to deploy a job to, users specify different configuration files which contain parameters and additional information so that Foundations can properly access and run model code on the environment.

## How to Deploy

Configuration files can live both globally on the machine or locally per Foundations project. When using the `foundations init` command, a default configuration file is [automatically created](../foundations_cli/#project-creation) in the `/config` directory. To set global environments, add `*.config.yaml` files to `~/.foundations/config`. You may need to create this directory first with:

```bash
mkdir ~/.foundations/config
```

Jobs can then be deployed to different environments in two ways:

<h3>1. Using the Foundations CLI</h3>
Running the following command will deploy jobs to user-specified environments:
```shellscript
$ foundations deploy --job-directory=/path/to/project --entrypoint=relative/path/to/entrypoint.py --env= --project-name
```
Foundations will first look for any `<env_name>.config.yaml` file in the `/config` directory that matches the specified `--env` argument. If a matching configuration file is found, Foundations will deploy the job to that specified environment. Otherwise, it will then look for the configuration in the global directory `~/.foundations/config` . If no configuration files are found, the command will return an error.

Available configuration files (and environments) can be found using:
```shellscript
$ foundations info --env
```

For more information on the Foundations CLI, please refer to the documentation [here](../foundations_cli/)

**Note:** If your code contains setting the environment via the notebook instructions below, this **will** override the selected environment by the deploy command.

<h3>2. Using SDK</h3>

In a separate script or notebook, you can deploy jobs with a variety of optional keyword args:  
```python
foundations.deploy(project_name=None, env='local', entrypoint='main.py', job_directory=None, params=None)
```

This will bundle everything from the job_directory and launches a new Foundations job to the specified environment. See the [SDK reference](../deploy/) for more information.

## Configuration Options

*Note: Typically, the Dessa team will provide tested and properly setup configuration files for deployment to the different environments which will not require users to modify any configuration options. In addition, if no `config.yaml` is provided, then Foundations will use built-in default values for job deployments*

### Define Environment 

**job_deployment_env**: specifies what environment to use for deploying jobs. Currently the supported environments are `local`, `ssh`, `gcp`, `aws`. 

For deployments to specific versions of the job orchestrator (scheduler), `scheduler_plugin` is used instead. This will be advised by the Dessa team if deemed necessary.

### Results Configurations

```yaml
results_config: {
    archive_end_point: /path/to/archives,
    redis_end_point: redis://someredis,
    artifact_path: /relative/path/to/artifact/tracking/directory
},
```

**archive_end_point**: defines full path to where to store results. The default is `local` which means it will use current project directory. For AWS and GCP deployments, this path can be specified with the following format: `<bucket>/path/to/archives`. By specifying the job_deployment_env, Foundations will automatically determine the right endpoint. 

Foundations also supports cross-environment storage for results. By specifying the URI schema of the desired endpoint, the job results can be stored in a different location from where the actual job was run. For example, if a job is deployed to GCP but you want to store the results in AWS, you can specify the full path with URI schema as: `s3://<bucket>/path/to/archives`

Supported URI schemas are: `gcp://`, `s3://`, `sftp://`, `local://`

**redis_end_point**: redis endpoint where we want to store results for faster reading

**artifact_path**: relative path where users can define a directory for Foundations to track. Files or artifacts written to that directory during runtime will be stored in the archive endpoint once the job is completed. 

### Cache Configurations

```yaml
cache_config: {
    end_point: /path/to/the/cache
},
```

**end_point**: defines full path to where to store cache files. The default is `local` which means it will use current project directory. For AWS and GCP deployments, this path can be specified with the following format: `<bucket>/path/to/cache`. By specifying the job_deployment_env, Foundations will automatically determine the right endpoint. 

Foundations also supports cross-environment storage for the cache. By specifying the URI schema of the desired endpoint, the cached functions can be stored in a different location from where the actual job was run. For example, if a job is deployed to GCP but you want to store the cached functions in AWS, you can specify the full path with URI schema as: `s3://<bucket>/path/to/cache`

Supported URI schemas are: `gcp://`, `s3://`, `sftp://`, `local://`

### Additional Configurations

For any SSH deployment (including GCP and AWS) to remote addresses, you'll need to define some additional values so that Foundations is able to SSH into the execution environment. Here's an example usage:

```yaml
ssh_config: {
    user: lou
    host: 11.22.33.44,
    port: 2222
    key_path: /path/to/the/keys,
    code_path: /path/to/the/code,
    result_path: /path/to/the/result,
}
```
**user** (*optional*): what user profile to access the remote server as. By default, it will use `foundations`.  
**host** (*required*): the remote machine ip address.  
**port** (*optional*): specifies what port the SSH service is listening to on the remote machine. By default uses port 22.  
**key_path** (*required*): the private key necessary for using SSH.   
**code_path** (*required*): the directory where jobs should be stored.   
**result_path** (*required*): the directory where job results should be stored after they've been run.  

<h3>log_level</h3>

Allowed values for `log_level` are `INFO`, `ERROR`, and `DEBUG`, just as in the `log_level` option described in the previous section.  Leaving it unset is the same as setting `INFO`.  Setting any other value will disable all logging for all non-job-related processes.

## Sample Configurations
```yaml
job_deployment_env: local
results_config: 
    archive_end_point: /path/to/archives
    redis_end_point: redis://someredis
    artifact_path: files

cache_config: 
    end_point: /path/to/the/cache

log_level: INFO
```

```yaml
job_deployment_env: ssh
results_config: 
    archive_end_point: /path/to/archives
    redis_end_point: redis://someredis

cache_config: 
    end_point: /path/to/the/cache

ssh_config: 
    host: 11.22.33.44
    key_path: /path/to/the/keys
    code_path: /path/to/the/code
    result_path: /path/to/the/result

log_level: DEBUG
```

```yaml
job_deployment_env: gcp
results_config: 
    archive_end_point: /<gcp-bucket>/path/to/archives
    redis_end_point: redis://someredis
    artifact_path: artifacts/models

cache_config: 
    end_point: /<gcp-bucket>/path/to/cache

ssh_config: 
    host: 11.22.33.44
    key_path: /path/to/the/keys
    code_path: /path/to/the/code
    result_path: /path/to/the/result

log_level: ERROR
```

```yaml
job_deployment_env: aws
results_config: 
    archive_end_point: /<s3-bucket>/path/to/archives
    redis_end_point: redis://someredis

cache_config: 
    end_point: /<s3-bucket>/path/to/cache

ssh_config: 
    host: 11.22.33.44
    key_path: /path/to/the/keys
    code_path: /path/to/the/code
    result_path: /path/to/the/result

log_level: INFO
```

```yaml
#Example config.yaml with storage to different remote location (gcp)

job_deployment_env: aws
results_config: 
    archive_end_point: gs://<bucket>/path/to/archives
    redis_end_point: redis://someredis

cache_config: 
    end_point: gs://<bucket>/path/to/cache

ssh_config: 
    host: 11.22.33.44
    key_path: /path/to/the/keys
    code_path: /path/to/the/code
    result_path: /path/to/the/result

log_level: INFO
```