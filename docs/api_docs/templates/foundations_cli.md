<h1>Foundations CLI Tool</h1>

The Foundations Command Line Tool provides users with a simple way to interact and manage projects in Foundations. The supported functionalities are listed below.

---
## Deploying Jobs

The Foundations CLI makes it easy to deploy jobs to different environments across different projects. 

```shellscript
$ foundations deploy [options]
```
<h3>Options</h3>
|   Option &nbsp;&nbsp;&nbsp;&nbsp;   | Description  |
|----|----|
| job-directory| The directory from which to deploy code from. Can be both relative or absolute paths. Foundations will bundle everything within this directory and treat this directory as where to run any code from, meaning any references to paths outside this directory will not be accessible. By default, Foundations will use your current working directory|
| entrypoint| The name and path of the main file to execute, relative to the job-directory. By default, Foundations will try to run `main.py` directly from the job-directory|
| project-name| The project name for job. By default Foundations will use the name of the current working directory|
| env| The deployment environment to run the job in. By default will run locally and look for global foundation deployment configurations|
| num-gpus| If your deployment environment has GPUs available, specifies number of gpus to allocate for job. Defaults to use one GPU|
| ram| The amount of RAM your job cap. By default foundations will download all stored artifacts from the root directory for a job|

Running this command with the right options will deploy your code into the specified Foundations deployment environment. Since you can specify the job-directory (which is the directory containing your source code + any other files needed to run an experiment), you can deploy a job from any directory on your machine. 

For example, if your current working directory is in the project root, you can deploy your `project_code` by specifying the proper options. Notice how the entrypoint is relative to the specified job-directory.

```
project
├── config
│   └── local.config.yaml
├── project_code
│   └── src
│       └── main.py   
```

To deploy the driver in the above example, run:
```shellscript
$ foundations deploy --job-directory=project_code --entrypoint=src/main.py --env=local
```

Foundations will first look for any `<env_name>.config.yaml` file in the `/config` directory that matches the specified `--env` argument. If a matching configuration file is found, Foundations will deploy the job to that specified environment. Otherwise, it will then look for the configuration in the global directory `~/.foundations/config` . If no configuration files are found, the command will return an error.

**Note:** Ensure your `entrypoint` does not include the following header, otherwise you will get an error:
```python
if __name__ == "__main__":
    etc.
```
---
##List Environment Information

Users can setup different deployment environments with Foundation (local, gcp, etc.) at both the project and global level. This allows users to customize their deployment environments and use a common one across multiple projects, or select specific environments per projects. Local configurations are stored in `/project_name/config`.

To set global environments, add `*.config.yaml` files to `~/.foundations/config`. If this directory doesn't exist, you will need to create this directory first with:

```bash
mkdir ~/.foundations/config
```

To identify the different deployment environments setup on the machine:

```shellscript
$ foundations info --env
```

List all available environments and their paths. 

If you are within your project directory, this command lists the names and the paths of both your local environments as well as your global environments.

```bash
#Example output for info --env command when in project directory
global configs:
env_name    env_path
----------  ----------
local       /home/newHomeDir/.foundations/config/local.config.yaml
 
project configs:
env_name    env_path
----------  ------------------------------------------------------------
default     /home/newHomeDir/foundations/hana/config/default.config.yaml
local       /home/newHomeDir/foundations/hana/config/local.config.yaml
```
Otherwise, this command will only list the names and paths your global environments:  
```bash
#Example output for info --env command when not in project directory
global configs:
env_name env_path
---------- ----------
local       /home/newHomeDir/.foundations/config/local.config.yaml
```

---
##Retrieve Job Logs

Users can retrieve logs from a remote deployed job, regardless of status, with the following command:

```shellscript
$ foundations retrieve logs --job_id=<deployed job_id> --env=<env_name>
```

This will return the logs of the job in its current state directly to the screen. For example, if the job is still running, the logs will be of the running jobs at the current point of execution. If the job is completed, it will be all the logs of the completed jobs.

Logs can also be stored to a file by piping:

```bash
$ foundations retrieve logs --job_id=12345 --env=gcp > 12345_log.txt
```

---
##Serve/Stop a Model Package

Users can serve a valid model package with the following command:

```shellscript
$ foundations serve start <job_id>
```
If no manifest file is found, an error will be returned. To stop a served package, run:

```shellscript
$ foundations serve stop <model_name>
```