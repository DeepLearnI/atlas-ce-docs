# Atlas CE on AWS

Being able to run Atlas CE on AWS means access to GPUs and faster results. In this tutorial we'll walk through setting up and running jobs on AWS with Atlas CE.

Requirements

* AWS account


## Create instance

First let's go to the AWS developer console, sign in, and then we'll create a new instance: [https://aws.amazon.com/console/](https://aws.amazon.com/console/)

Go to Services > EC2, then click the **"Launch Instance"** button to start setup.

### Step 1: Choose an Amazon Machine Image (AMI)

Let's use the custom Atlas CE AMI, to do this:

* Select "Community AMIs" on the left sidebar
* Search for "Atlas CE"
* Select the AMI that says "Atlas Community Edition on Deep Learning AMI for Ubuntu
"

![Select AMI](../../assets/images/aws-select-ami2.png)

Our custom AMI is just AWS's Deep Learning AMI (Deep Learning AMI (Ubuntu 16.04) Version 24.2) with Atlas CE added on top of it.

!!! note
    Once the instance has been finalized and spun up, costs will be incurred. Please follow the tear down steps at the bottom of this guide to minimize this.

### Step 2: Configure an Instance Type

For this page we'll select a *p2.xlarge* instance type, as we want some a GPU to train with. We recommend a P2 instance as it a good balance between performance and cost, but if you are looking for more power you can select a P3 instance.

![Instance type](../../assets/images/aws-instance-type.png)

Make sure to click **"Next: Configure Instance Details"** to continue provisioning the instance.

### Step 3: Configure Instance Details

* If your instance does require additional configuration adjust as needed
* Otherwise there are no changes needed here, just click **"Next: Add Storage"**

### Step 4: Add Storage

We recommend increasing the size of your storage to at least 250GB, as the base AMI image is already ~80GB. Adjust as needed for your expected data.

![Add storage](../../assets/images/aws-add-storage.png)

### Step 5: Add Tags

* No changes, just click **Next: Configure Security Group**

### Step 6: Configure Security Group

Next, we'll create a new security group to allow for Atlas to securely use a few different ports on our instance. Specifically to allow the GUI, REST API, and archive server.

To allow for this, add the following 3 new rules for the below ports, and for each rule change the "Source" to **My IP**.

| Type | Protocol | Port Range | Source | Description
|-----------|----------|-----------|-----------|----------|
| SSH | TCP | 22 | My IP (will default to instance IP) | (can leave empty)
| Custom TCP Rule | TCP | 5555 | My IP (defaults to instance IP) | (can leave empty)
| Custom TCP Rule | TCP | 5557 | My IP (defaults to instance IP) | (can leave empty)
| Custom TCP Rule | TCP | 5959 | My IP (defaults to instance IP) | (can leave empty)

Now, click **Review and Launch** to go review our instance before launching. 

### Review Instance Launch

Our instance setup should now look similar to the below.

![Review ](../../assets/images/aws-review-instance-launch.png)

Click "Launch" which should then ask you to create a new key pair. Select "Create a new key pair" and give it the name "atlas-ce", and then download the key pair, then click Launch Instances". It should then redirect you to the Launch Status page. Click on your instance name to go to the **Instances** page, which you can then find the IPv4 address of the instance in the lower **Description** panel.

![aws now launching](../../assets/images/aws-now-launching.png)

You should then be able to use your downloaded `.pem` key to then SSH into the instance to check that everything is setup.

Be sure to run `chmod 400 <key_name>.pem` on your key before SSH'ing to give it the proper permissions. We also recommend that you move the key to your `~/.ssh/` directory.
 
`ssh -i /path/to/key/<key_name>.pem  ubuntu@ipv4.of.ec2.instance`

When you first SSH in, the instance will run a few commands which includes activating a conda environment that contains `atlas-server` and `foundations`. It also runs `atlas-server` so all the services for Atlas CE are running.

You should also now be able to see the GUI. In your browser go `<ipv4.of.ec2.instance>:5555` and you should see the Atlas CE project page. It'll be empty, so let's start by creating our first project.

### Run our first Atlas CE job

If this is your first time using Atlas CE, you can try run a simple job with the following steps. Or you can just skip ahead to setting up AWS to remotely work with VSCode below.

To create a simple job to run within the AWS instance we'll need to do the following:

* Activate the conda environment to run Atlas CE: `conda activate atlas_ce_env`

Now you should have access to `foundations` CLI. Next we'll create a template project and run it with Foundations.

* Run `foundations init my-atlas-project`
* This will create directory `<project_name>` with a scaffolded simple job to run
* `cd` into the `/my-atlas-project` directory
* run `foundations submit scheduler . main.py`
* Go back to the Atlas CE GUI in your browser, and you should see your first project that can be explored

For more information on the Foundations CLI read our CLI section, or run `foundations --help`.

We've now successfully setup a P2 instance with Atlas! In the next section we'll go over running jobs on AWS with VSCode.

## Running jobs remotely via VSCode

A really easy to develop with Atlas locally in VSCode, while having the power of a cloud GPU, is the setup remote deployment in VSCode. This will allow for our code to be synced with our instance, and simply type the `foundations submit` command to run jobs.

Requirements:

* Install [VSCode](https://code.visualstudio.com/)

First, open up VSCode, and we'll install the [Remote - SSH plugin](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-ssh) that will allow us to open code from the remote instance in VSCode

Once the plugin is installed open the Command Palette and select "Remote-SSH: Connect to Host"

![VSCode plugin ](../../assets/images/vscode-install-plugin.png)

It will then prompt us to "Add New SSH Host...', where we'll enter the host and user of the instance like so:

`ubuntu@<my.aws.ip.address>`

It should open a new VSCode window where we'll be able to select "File" > "Open..." and then select a directory from our instance to open. In our case we can select our `my-atlas-project` which will then open up in VSCode in a new window.

At the bottom the VSCode window we'll select the "Terminal" tab, and choose "bash" from the drop down that will give us bash shell access to AWS.

Let's first activate the conda environment that comes with the AMI:

* `conda activate atlas_ce_env`
* cd into `my-atlas-project`
* Let's test that we can run our simple job with  `foundations submit scheduler . main.py`
* You should see this job in the Atlas CE GUI

![vscode shell ](../../assets/images/vscode-bash-submit.png)

We're now set! We can now open `model.py` and adjust as we wish, or you can start on your own project.

If you're looking for more advanced docs on setting up VSCode with AWS, Microsoft has a good setup [guide](https://code.visualstudio.com/docs/remote/ssh#_remembering-hosts-you-connect-to-frequently) with much more detail.

## Tear down AWS instance

It's important to be aware that after the instance has been spun up you will incur costs on your account. There are two options: either stop the instance (which will mean costs are minimal to keep your storage around), or throw away the instance completely.

To stop or terminate the instance:

* Go to your AWS console
* Right click on our P2 instance > "Instance State" > either Terminate or Stop

![Review ](../../assets/images/aws-stop-instance.png)

That's it, we've successfully spun up a GPU instance and run a few jobs remotely from VSCode!

You can now either start your own projects, or look at some of our more advance tutorials to explore more of Atlas CE.

### Questions

If you have any thoughts or feedback about setting up Atlas CE on AWS we're always happy to help answer questions on our [Dessa Community Slack](https://dessa-community.slack.com/join/shared_invite/enQtNzY5MTA3OTMxNTkwLWUyZDYzM2JmMDk0N2NjNjVhZDU5NTc1ODEzNzJjMzRlMDcyYmY3ODI1ZWMxYTQ3MzdmNjcyOTVhMzg2MjkwYmY)!
