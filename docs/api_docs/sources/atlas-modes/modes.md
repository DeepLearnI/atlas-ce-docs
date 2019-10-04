<h1>Atlas Walkthrough</h1>
---
### Setup
To get started with Atlas, activate the virtual environment (if any) that was used to install Atlas server. Next, let's make sure Atlas Server is running by doing:
`atlas-server start`

*Note: Alternatively, you can use `atlas-server start -g` to bring up Atlas server with GPU support*

This will bring up all of the Atlas services, including the GUI which is available at [http://localhost:5555](http://localhost:5555) by default.

### Modes of Operation
Atlas runs in two modes.

#### 1. **Execution**:
(Use this mode for single runs, manual parameter tuning, and small experiments) <br><br>
In execution mode, code is run in an existing local environment that you already have setup. Atlas provides experiment version control, tracks your experiments and any associated metadata (e.g. hyper-parameters, metrics, artifacts) that you choose to track.

#### 2. **Scheduling**:
(Use this mode if you want to schedule many jobs and do a large hyperparameter search) <br><br>
In scheduling mode, Atlas CE queues your experiment with the local Atlas scheduler which runs it in a containerized environment. This mode gives you the ability to queue a large number of experiments as well as leverage common containerized tools such as NVIDIA Rapids.


### GPU Visibility
By default, Atlas CE does not provide access to the GPUs on the machine. Luckily, if you are hoping to run this on a machine and use the GPUs, it's pretty simple.

Just run `atlas-server start -g` and you're off to the races.

**What does this mean?**

Running with GPUs enabled actually provides 2 main benefits: 

 1: Jobs will have access to your machines GPUs
 
 2: There will be as many Atlas workers as GPUs available to Atlas, allowing you to run multiple jobs at once
 
!!! danger "Important Usage Information"
    This can be very exciting, especially if you have a really powerful machine that you want to use to make the worlds next AlexNet, but with great power comes great responsibility! Below are some gotchas that you should watch for:
    
    - Although Atlas makes sure that a job given 1 GPU can only access that GPU, we don't keep track of RAM or CPU usage and your jobs could clash on those resources if not careful
    - This feature doesn't magically make your code use all available GPUs, it just makes those GPUs available for your code to use

**How to launch jobs that use GPUs**

We have given Atlas access to GPUs, but by simply running `foundations submit scheduler . main.py`, we still haven't given the job access to the GPUs — we have to use a special argument `--num-gpus #`.
If you are using the Python SDK, you can pass `num_gpus=#` to the `foundations.submit()` command.

!!! note "Queue Priority"
    The scheduler uses a fairly simplistic process for allocating jobs — in which we only get the next job in the queue.
    
    This means that if Atlas has access to 4 GPUs, with 4 workers, and your queue looks like: 
    
    - Job1(num_gpus=2), Job2(num_gpus=2), Job3(num_gpus=3), Job4(num_gpus=3), Job5(num_gpus=1)
    
    Job1 and Job2 will run, both taking 2 GPUs. Job3 will hold up the rest of the queue since there are not 3 GPUs available. 
    
    Once Job1 and Job2 stop, Job3 will start running with 3 GPUs. Job4 will hold up the rest of the queue since it doesn't have enough resources.
    
**Limiting GPU access to Atlas**

By default Atlas will have access to all GPUs on the host machine. You can specify specific GPU availability by setting the `CUDA_VISIBLE_DEVICES` environment variable ([more information](https://devblogs.nvidia.com/cuda-pro-tip-control-gpu-visibility-cuda_visible_devices/)).

`CUDA_VISIBLE_DEVICES` takes in a comma separated string of numbers, where each number is the ID of the GPU you wish to make visible to Atlas.

You can export this variable in the same shell right before starting Atlas:

 1. `export CUDA_VISIBLE_DEVICES=0,1`
 2. `atlas-server start -g`
 
Or set the variable in the Atlas start command:

 1. `CUDA_VISIBLE_DEVICES=0,2 atlas-server start -g`