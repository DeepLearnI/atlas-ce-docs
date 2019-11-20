# Atlas Team AWS Setup Instructions

## Prerequisite
Company to send Dessa their AWS Account Number for AMI sharing

Dessa to share access to Atlas Team master and worker AMIs

## Steps

**1) Create an AWS EFS filesystem**

* This will hold files that need to be shared between instances.
* The only requirement is that the master and worker instances can mount to this filesystem.

**2) Start an instance with the master AMI — specifying tags provided by Dessa.**

* This machine will not run any jobs and therefore does not need large resources.
* Tags will be used by the underlying AMI for proper configuration.

**3) Start n amount of instances with the worker AMI — specifying tags provided by Dessa.**

* These machine types are defined by the workloads that your organization will be running.
* Tags will be used by the underlying AMI for proper configuration.

**4) Log into the admin account interface and change the password.**

* A default admin account is created without secure credentials.
* On startup, the admin should change the password.

**5) Create user accounts through the web interface.**

For full details on user management see the User Management section of these docs.

**6) Have users “pip” install the Foundations Python SDK on their work machines.**

**7) Give users the configuration file generated on the master machine.**

* This file will sit on every clients that needs to talks to the master machine. It will point to the master instance, allowing the user to submit jobs to the cluster.

**8) Have users login on their work machine.**

There are two different ways for a user to interact the Atlas authentication.

* Using the foundations CLI: `foundations login`, which will prompt the user for username and password.
* Using the foundations GUI: a token will be created on login — tokens can be managed through the admin account interface.

**9) Launch jobs!**