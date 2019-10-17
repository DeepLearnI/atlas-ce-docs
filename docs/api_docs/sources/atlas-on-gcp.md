# Atlas CE on GCP

Being able to run Atlas CE on GCP means access to GPUs, and more importantly faster model results. In this tutorial we'll walk through setting up and running jobs on GCP with Atlas CE, as well as running experiments from VSCode.

Requirements

* GCP account
* gcloud CLI tool installed (<a target="_blank" href="https://cloud.google.com/sdk/downloads/">download</a>)


### Step 1: 

First let's go to the GCP developer console, sign in, and then we'll create a new instance using the: <a target="_blank" href="https://console.cloud.google.com/marketplace/details/click-to-deploy-images/deeplearning">GCP Deep Learning VM</a>.

This VM will give us access to an instance with a GPU, as well as built-in libraries like Docker, and Tensorflow.

Click the **"Launch on compute engine"** button to start setup.

![create instance](../assets/images/gcp-create-instance.png)

### Step 2: Deployment settings

There's a few updates we'll need to make to the instance before we deploy it:

* Set a deployment name
* Zone: select a zone that with K80 GPUs available (for our use, we'll select **us-east1-c**)
* Machine Type: the default of 2 vCPUs, with 13 GB of memory is fine
* GPUs: select 1 NVIDIA Tesla K80 GPU
* Framework: nothing to change here
* GPU: check the **"Install NVIDIA GPU driver automatically on first startup"** box to make sure we have access to the GPUs
* Boot disk: can keep as "Standard Persistent Disk"
* Boot disk size: we'll bump this up to 150GB
* Networking: nothing to change

!!! note
    K80 GPUs are not the most powerful, but for most simple uses of GPUs it should suffice. If you're doing data intensive work you may want to select an instance with a P100 GPU

We should now be good to spin up the instance, just click the **Deploy** button.

It will take about 5 minutes for the instance to initialize.

### Step 3: Setup Atlas CE

Use the provided gcloud CLI command to SSH into the instance. It should look similar to:

![SSH into instance](../assets/images/gcp-ssh-instance.png)

We can take this command and run it in our terminal to SSH into the instance. Make sure you have the gcloud CLI tool setup prior to doing this.

Once inside the instance we now need to install Atlas CE. We've put together a script that does a lot of the leg work (create environments and installing Atlas CE).

* To get the script, we'll run `wget https://gist.githubusercontent.com/pippinlee/d2b98a7ff058e66b558bfb331f3a4635/raw/36e6119935180e232437107fd8a77e7c2a40841b/install_atlas.sh`. This will give us the Atlas CE installer file
* Running `bash install_atlas.sh` will install Atlas CE and start it running within Docker
* Next we'll source the conda environment created by Atlas by running `source ~/.bashrc` and then `conda activate atlas_ce_env`

Now Atlas CE is running and you'll have access to both the `foundations` and `atlas-server` CLI.

You should now be able to view the Atlas Dashboard by going in your browser to `<external.ip.of.your.instance>:5555`. If you ever need to find the IP of your instance you can find it on your GCP console <a target="_blank" href="https://console.cloud.google.com/compute/instances">instance list</a>).

![SSH into instance](../assets/images/gcp-ssh-ip.png)

In the dashboard's project page your should see a project that has been run once. These projects were baked into the script to help get started.

### Run our first Atlas CE job

If this is your first time using Atlas CE, you can try run a simple job with the following steps. Or you can just skip ahead to setting up GCP to remotely work with VSCode below.

We can run one of our demo projects to try out how the `foundations` CLI works.

* `cd atlas-tutorials/auction_price_regression_tutorial`
* Run `foundations submit scheduler . driver.py`
* Go back to the Atlas CE GUI in your browser, and you should see the new job we've just run

For more information on the Foundations CLI read our CLI section, or run `foundations --help`.

We've now successfully setup an Deep Learning VM instance with Atlas! In the next section we'll go over running jobs on GCP with VSCode.

## Running jobs remotely via VSCode

A really easy to develop with Atlas locally in VSCode, while having the power of a cloud GPU, is the setup remote deployment in VSCode. While we also love PyCharm's remote deployment, it's not free, so we'll just use VSCode. This will allow for our code to be synced with our instance, and simply fun `foundations submit ...` commands to run jobs.

Requirements:

* Install <a target="_blank" href="https://code.visualstudio.com/">VSCode</a>

First, open up VSCode.

Before we connect to the host in VSCode, let's open the SSH config file, to add this instance to our SSH Config, to easily allows VSCode to connect to our instance.

* Open ~/.ssh/config

Add the following lines:

```
Host <my.gcp.ip.address>
 IdentityFile ~/.ssh/google_compute_engine
 User <username>
```

Once the you've updated the SSH config, open the Command Palette and select "Remote-SSH: Connect to Host".

* Open Command Palette in VSCode: `Cmd + Shift + P` (or click green "Open Remote Window" botton, bottom left of VSCode)
* Will then prompt us to "Add New SSH Host...', where we'll enter the host and user of the instance like so:

`ssh <username>@<my.gcp.ip.address>`

It should open a new VSCode window where we'll be able to select "File" > "Open..." and then select a directory from our instance to open. In our case we can select our `atlas_tutorials/auction_price_regression_tutorial` project which will then open up in VSCode in a new window.

At the bottom the VSCode window we'll select the "Terminal" tab, and click the "+" symbol to open a new shell tab. Choose "bash" from the drop down that will give us bash shell access to GCP.

* cd into `atlas-tutorials/auction_price_regression_tutorial`
* Activate the environment with `conda activate atlas_ce_env`
* Let's test that we can run a job with  `foundations submit scheduler . driver.py`
* You should see this job in the Atlas CE GUI

![vscode shell ](../assets/images/gcp-vscode.png)

We're now set! You can now open the files and adjust as you wish, or you can start on your own project. To understand more about the `auction_price_regression` project, you can check out the full tutorial in the **Tutorial** section of the docs.

If you're looking for more detailed docs on setting up VSCode to remotely run code, Microsoft has a good setup <a target="_blank" href="https://code.visualstudio.com/docs/remote/ssh#_remembering-hosts-you-connect-to-frequently">guide</a> with much more detail.

## Tear down GCP instance

It's important to be aware that after the instance has been spun up you will incur costs on your account. There are two options: either stop the instance (which will mean costs are minimal to keep your storage around), or throw away the instance completely.

To stop or terminate the instance:

* Go to your VM instances console
* Find your instance > click either Delete or Stop

![Review ](../assets/images/gcp-stop-instance.png)

That's it, we've successfully spun up a GPU instance and run a few jobs remotely from VSCode!

You can now either start your own projects, or look at some of our more advance tutorials to explore more of Atlas CE.

### Questions

If you have any thoughts or feedback about setting up Atlas CE on GCP we're always happy to help answer questions on our <a href="https://dessa-community.slack.com/join/shared_invite/enQtNzY5MTA3OTMxNTkwLWUyZDYzM2JmMDk0N2NjNjVhZDU5NTc1ODEzNzJjMzRlMDcyYmY3ODI1ZWMxYTQ3MzdmNjcyOTVhMzg2MjkwYmY" target="_blank">Dessa Community Slack</a>!