# Quick Start Guide

### Installation

*Estimated time: 3 minutes*

**Prerequisites**

 1. Docker version \>18.09 ([Docker installation instructions](https://docs.docker.com/install/))
 2. Python \>3.6
 3. \>5GB of free machine storage
 4. The `atlas_ce_installer.py` file

Atlas CE currently supports Mac OSX, Linux & Windows 10.

!!! tip 
    Windows 10 Home edition users can set up Atlas CE by installing [Docker Toolbox](https://docs.docker.com/toolbox/toolbox_install_windows/).
    Windows 10 Enterprise edition users should use [Docker for Windows](https://docs.docker.com/docker-for-windows/).

**Common**

 1. Create a new, empty directory where you will install Atlas CE.

 2. Copy the `atlas_ce_installer.py` file into this directory.

 3. Create and activate a Python \>3.6 virtual environment using 
 [Conda](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-with-commands)
 or [venv](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)
 to minimize dependency issues.

 4. Follow you OS-specific instructions below.

**Linux/OSX**
 1. Run the install script with `python atlas_ce_installer.py`.
 
**Windows 10**
 1. Install the following python package into the environment created in step 3: `pip install pypiwin32=223`

 2. Run the install script with `python atlas_ce_installer.py`

 3. [Windows 10 Home only]: 
    - Open Oracle VirtualBox.
    - Right-click on the docker VM and click on `Settings`.
    - Select 'Network' in the configuration pane, expand the `Advanced` section and click on `Port Forwarding`.
    - Add the following port forwarding rules:

| Name | Protocol | Host IP | Host Port | Guest IP | Guest Port |
|-----------|----------|-----------|-----------|----------|------------|
| Scheduler | TCP | 127.0.0.1 | 5000 |  | 5000 |
| GUI | TCP | 127.0.0.1 | 5555 |  | 5555 |
| Tracker | TCP | 127.0.0.1 | 5556 |  | 5556 |
| Archive | TCP | 127.0.0.1 | 5557 |  | 5557 |
| Tboard | TCP | 127.0.0.1 | 5959 |  | 5959 | 

!!! tip 
    Running `python atlas_ce_installer.py --help` will give you troubleshooting advice if the script isn't working as expected.


!!! tip
    The longest part of the script is pulling the Atlas CE docker images, if the script fails at this point, 
    you can re-run it using `python atlas_ce_installer.py -dp` to skip over the download and unpacking and go directly to the image pull.

---

### Start-up

After completing the [installation section](#installation), you can do the following to start Atlas CE:

 1. Validate that you are in the same Python environment that was used to run the installation script.
 2. Run `atlas-server start`.
 
!!! tip
    You can also start Atlas Server with GPU support by running `atlas-server start -g`. This will allow Atlas to use all CUDA-enabled GPUs on your system.  
 
!!! success
    Validate that the GUI is running by going to the [GUI](http://localhost:5555). This is your centralized location to track all of your experiments.

---

### Hello Atlas

After completing the [start-up section](#start-up), follow the next few steps to launch your first Atlas CE job:

 1. Navigate to where you'd like to create your Atlas project directory.
 2. Ensure that you are in the environment that was used during installation.
 2. Run `foundations init hello-atlas` to create an example project.
 3. Navigate into the newly created `hello-atlas` directory.
 4. Run the sample code provided by running `python main.py`.
 5. Head to the [GUI](http://localhost:5555/projects) to see your experiment!


!!! Note
    When you run a job for the first time, it will download the appropriate worker image needed. <br>This will take roughly 1.5 minutes.
