<h1>Atlas Walkthrough</h1>
---
### Setup
To get started with Atlas, activate the virtual environment (if any) that was used to install Atlas server. Next, let's make sure Atlas Server is running by doing:
`atlas-server start`

*Note: Alternatively, you can use `atlas start -g` to bring up Atlas server with GPU support*

This will bring up all of the Atlas services, including the GUI which is available at [http://localhost:5555](http://localhost:5555) by default.

### Modes of Operation
Atlas runs in two modes.

#### 1. **Execution**:
(Use this mode for single runs, manual parameter tuning, and small experiments) <br><br>
In execution mode, code is run in an existing local environment that you already have setup. Atlas provides experiment version control, tracks your experiments and any associated metadata (e.g. hyper-parameters, metrics, artifacts) that you choose to track.

#### 2. **Scheduling**:
(Use this mode if you want to schedule many jobs and do a large hyperparameter search) <br><br>
In scheduling mode, Atlas CE queues your experiment with the local Atlas scheduler which runs it in a containerized environment. This mode gives you the ability to queue a large number of experiments as well as leverage common containerized tools such as NVIDIA Rapids.
