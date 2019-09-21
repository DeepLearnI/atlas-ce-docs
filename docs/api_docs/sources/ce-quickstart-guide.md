# Quick Start Guide

### Installation

*Estimated time: 20 minutes (depending on internet connection)*

**Prerequisites**

 1. Docker version \>18.09

 2. Python \>3.6

 3. \>10GB of free machine storage

 4. The `atlas_installer.py` file

**Installation Steps**

 1. Create a new, empty directory where you will install Atlas CE
 2. Copy the `atlas_installer.py` file into this directory
 3. [Optional] Create and activate a Python \>3.6 virtual environment to minimize dependency issues
 4. Run the install script with `python atlas_installer.py`
 
> TIP: Running `python atlas_installer.py --help` will give you troubleshooting advice if the script isn't working as expected. 


> TIP: The longest part of the script is downloading the Atlas CE package, if the script fails after this package is
downloaded, you can run it using `python atlas_installer.py -d` to skip the download step and use the local file. 

---

### Start-up

After completing the installation step, you can do the following to start Atlas CE:

 1. Validate that you are in the same Python environment that you ran the installation script in
 2. Run `atlas-server start`. You can also start Atlas Server with GPU support by running `atlas-server start -g`_
 3. Validate the GUI starting up by going to the [GUI](http://localhost:5555)

---

### Hello, Atlas

After completing the start-up steps, follow the next few steps to launch your first Atlas CE job!

 1. Navigate to where you'd like to create your Atlas project directory
 2. Run `foundations init hello-atlas` to create an example project
 3. Navigate into the newly created `hello-atlas` directory
 4. [Optional] Feel free to look at the code and files; `main.py` is a good starting place
 5. Run the sample code provided by running `python main.py`
 6. Head to the [GUI](http://localhost:5555/projects) to see what we just launched!
