# Atlas Team AWS Setup Instructions

The following document outlines how to setup and deploy a multi-node compute system that runs Atlas Team, including the Keycloak authentication system to AWS.

## Prerequisite
* AWS account for admin

## Setup:

Atlas will need a master node instance, worker instance node(s), as well as an EFS filesystem.

### Creating master instance on AWS

In order to setup Atlas, we'll first create the master instance that will be in charge of storing and managing the job queue.

### Step 1: Choose an Amazon Machine Image (AMI)

* Search for the "DeepLearning AMI" that uses Ubuntu 16.04

### Step 2: Configure an Instance Type

For this page we'll select a *t2 medium* instance type.

![Instance type](../assets/images/aws-instance-type.png)

Make sure to click **"Next: Configure Instance Details"** to continue provisioning the instance.

### Step 3: Configure Instance Details

* If your instance does require additional configuration adjust as needed
* Otherwise there are no changes needed here, just click **"Next: Add Storage"**

### Step 4: Add Storage

We recommend increasing the size of your storage to at least 250GB. Adjust as needed for your expected data.

![Add storage](../assets/images/aws-add-storage.png)

### Step 5: Add Tags

* No changes, just click **Next: Configure Security Group**

### Step 6: Configure Security Group

Next, we'll create a new security group to allow for Atlas to securely use a few different ports on our instance. Specifically to allow the GUI, REST API, and archive server.

To allow for this add the following 4 new rules:

* Type: `NFS`, port: `2049`, source: `<Name of security group>`
* Type: `Custom TCP`, port: `5555`, source: `My IP` 
* Type: `Custom TCP`, port: `5558`, source: `My IP`
* Type: `Custom TCP`, port: `8443`, source: `My IP`

![Add storage](../assets/images/atlas-team-security-group.png)

Now, click **Review and Launch** to go review our instance before launching. 

### Review Instance Launch

Our instance setup should now look similar to the below.

<!-- ![Review](../assets/images/aws-review-instance-launch.png) -->


* Click "Launch" which should then ask you to create a new key pair
* Select "Create a new key pair" and give it the name "atlas-team" (note: if you've already used this key name before you can either re-use of, or create another unique key name)
* Download the key pair
* Click "Launch Instances"
* It should then redirect you to the Launch Status page
* Beside "The following instance launches have been initiated" you should see your new instance ID. Click the ID to go to the **Instances** page
* You can find the public IPv4 address of the instance in the lower **Description** panel.

![aws now launching](../assets/images/aws-now-launching.png)

You should then be able to use your downloaded `.pem` key to then SSH into the instance to check that everything is setup.

Run `chmod 400 <key_name>.pem` on your key before SSH'ing to give it the proper permissions. We also recommend that you move the key to your `~/.ssh/` directory.


### Create an EFS filesystem

We'll also need to setup an EFS filesystem that we can use as a central storage location.

* When configuring the EFS filesystem for each availability zone add it to the security group that was  previously created and added to the master instance.
* After creation it will provide a few commands that will mount the filesystem. You'll need the `sudo mount -t nfs4...` command in a few steps, so either copy it or keep this tab open for easy access.

![efs creation](../assets/images/atlas-team-efs.png)

### Installing and setting up Atlas

The following outlines how to setup Atlas on the master node:

* SSH into the master instance `ssh -i /path/to/key/<key_name>.pem  ubuntu@ipv4.of.ec2.instance`

* Download the installer onto the instance (both the atlas_installer.py and atlas_team.tgz)

* Create a conda environment: `conda create -y -n atlas-team python=3.6.8`

* Activate the conda environment `conda activate atlas-team`

* Run the installer: `python atlas_installer.py -dl`

* Backup `~/.foundations` directory: `cp -r ~/.foundations ~/.BACK_foundations`

* Mount the EFS system to `~/.foundations`. Do this by using the mount command that was provided after creating the EFS filesytem: `sudo mount -t nfs4 -o nfsvers=4.1,rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2,noresvport fs-b563e834.efs.us-east-1.amazonaws.com:/ ~/.foundations`

* Copy the content of the backed-up directory back (cp -r ~/.BACK_foundations/* ~/.foundations)

* Create a directory as follows: `mkdir ~/f9s_work_dir`

### Updating master node configurations

**~/.foundations/config/local_docker_scheduler/database.config.yaml**

* Update to use the Master nodes Private IP in all 4 `host` fields and `5556` in all `port` fields

**~/.foundations/config/local_docker_scheduler/tracker_client_plugins.yaml**

* Update to use the Master nodes Private IP in the `host` field and `5556` in the `port` field

**~/.foundations/config/local_docker_scheduler/worker_config/execution/default.config.yaml**

* Replace `atlas-ce-tracker` with the Master nodes Private IP and `6379` with `5556`

**~/.foundations/config/local_docker_scheduler/worker_config/submission/scheduler.config.yaml**

* Replace `atlas-ce-local-scheduler` with the Master nodes Private IP and the value for `working_dir_root` to be `/home/ubuntu/f9s_work_dir`

**~/.foundations/config/submission/scheduler.config.yaml**

* Change `working_dir_root` to be `job_store_dir_root`

* Add a field `working_dir_root: /home/ubuntu/f9s_work_dir` at the bottom

### Starting Atlas Server

Set environment variables

* `export HOST_ADDRESS=http://<MASTER-NODE-PRIVATE-IP>:5000/`

* `export REDIS_ADDRESS=<MASTER-NODE-PRIVATE-IP>`

* `export NUM_WORKERS=0`

* Now run `atlas-server start` to start the Atlas server

### Log into Atlas's authentication system

Atlas runs a Keycloak authentication server for managing users and login.

* Login to Keycloak via the admin console: `https://<master_node_external_ip>:8443`. When first spun up the username and password are both `admin`

* We recommend changing the admin password upon first login


### Setup the worker node

For our multi-node system, we can spin up as many worker instances as needed. Below we'll walk through setting up on one instance. Repeat as needed.

1. Create a Worker EC2 instance using the Ubuntu 16.04 Deeplearning AMI (p2.xlarge recommended)

2. SSH into the worker instance `ssh -i /path/to/key/<key_name>.pem ubuntu@ipv4.of.ec2.instance`

3. Download the installer onto the instance (both atlas_installer.py and atlas_team.tgz)

4. Create a conda environment: `conda create -y -n atlas-team python=3.6.8`

5. Activate the conda environment: `conda activate atlas-team`

6. Run the installer: `python atlas_installer.py -dl`

7. Mount the EFS system to `~/.foundations`. Do this by using the mount command that was provided after creating the EFS filesytem: `sudo mount -t nfs4 -o nfsvers=4.1,rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2,noresvport fs-b563e834.efs.us-east-1.amazonaws.com:/ ~/.foundations`

8. Set environment variables
    * `export HOST_ADDRESS=http://<NODES-IP>:5000/`
    * `export REDIS_ADDRESS=<MASTER-NODE-PRIVATE-IP>`
    * `export NUM_WORKERS=1`

9. Run `atlas-server start`