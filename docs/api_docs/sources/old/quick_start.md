<h1>Quick-Start Guide</h1>

Welcome to the Foundations quick-start guide! The following instructions should help you get setup with Foundations as quick as possible and ready to run your first job on your local machine. For more information on any of the steps, please refer to the full [installation](../start_guide/) guide.

#Installation Prerequisites

Before getting started, you will need Python 3.x installed on your machine. If you plan to use Tensorflow, we recommend using versions <= `Python 3.6` as it does not support versions greater at the moment. 

<h3>macOS/Linux</h3>

To run Foundations, you will need [Docker](https://docs.docker.com/docker-for-mac/install/) ( Version >= 18.09 )   

We also recommend using [Anaconda](https://www.anaconda.com/distribution/#macos) ( Python 3.x version ) to setup a virtual environment where all packages can be installed and maintained with ease.

<h3>Windows</h3>

Before getting started with Foundations, you will need the following tools on your machine:  

* [Anaconda](https://conda.io/miniconda.html) ( Python 3.x version )  
* [Docker](https://docs.docker.com/docker-for-windows/install/) ( Version >= 18.09 )  
* [Git Bash](https://git-scm.com/download/win)  

To run Foundations correctly, you will need to setup the environment from an Anaconda prompt, then use Git Bash to setup the GUI (optional) and deploy jobs.

<h3>Setup Access to Dessa Private Repository</h3>
To setup Foundations, you will first need access to the Dessa private pip and docker repositories. Please reach out to the Dessa team for necessary credentials.

For Pip access, you will need a `pip.conf` or `pip.ini` with credentials to Dessa's private pip repository. This file should be placed in `~/.config/pip/pip.conf` (macOS/Linux) or `~/AppData/Roaming/pip/pip.ini` (Windows).

For Docker access, this can be setup with the command: `docker login <DESSA DOCKER DOMAIN>` and following the prompts. 

## 1. Setup Conda Environment
To setup Foundations, we recommend establishing a virtual environment where all packages can be installed and maintained with ease. They also isolate the dependencies of different individual projects, avoiding Python version conflicts and prevent permission issues for non-administrator users.

For this tutorial, we will be using ```Anaconda``` to setup Foundations; however, other package managers such as `venv` or `pyenv` can be used as well. To create a new python environment, run the following commands in either terminal (macOS/Linux) or in a new Anaconda prompt (Windows):
```bash
conda create --name foundations_env python=3.6
```

*Note:* We use Python 3.6 since Tensorflow only supports up to 3.6 at the moment.

Next, activate the environment by running:
```bash
conda activate foundations_env
```

To deactivate the environment you are using with Foundations, you can run:
```bash
conda deactivate
```

For additional information on managing Conda envionments, please refer to the documentation [here](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)

## 2. Install Foundations
For Windows users, please open a new git bash prompt, we will be using git bash as our primary interface for all commands for the rest of the tutorial.

To install the latest version of Foundations, run:

```bash
pip install dessa-foundations
```

To check that Foundations is installed, you can verify that the Foundations CLI tool is available with:
```bash
$ foundations
```

For more information about getting access, please reach out to the Dessa Integrations team.

## 3. Setting up Redis and GUI (local deployment only)

Foundations uses [Redis](https://redis.io/) as a quick and efficient way to store data for experiments. This, as well as the Foundations GUI for visualizing experiments, can be setup with a Foundations CLI command:

```bash
$ foundations setup
```

Once completed, you will be able to visit your running GUI at `https://localhost:6443`, which helps visualze all your projects, experiments, and metrics.

**Note: Other instances of Redis on the same machine may interfere with the setup through Docker.** For more information please reference the Redis [guide](../start_guide/#redis-setup). In addition, you will need access to the private docker repository containing the Foundation GUI images. 

## 4. Starting Your First Project

That's it! Foundations should now be setup and ready to use on your local machine. For a step-by-step guide on your first project, check out our [step-by-step guide](../first_example/).