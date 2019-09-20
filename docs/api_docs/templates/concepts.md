<h1>Foundations Concepts</h1>

Foundations' core philosophy is to non-intrusively integrate with how you work and do the heavy-lifting for you, so that you can do more machine learning with less effort.  

It's designed to work with any machine learning library or code, and requires little or no refactoring to integrate into an existing codebase. Furthermore, Foundations' provides an standard interface to bring models into production so you can *track*, *manage*, and *deploy* any machine learning code in a reproducible and reusable way across different teams.

To better understand how Foundations works, here are some concepts on how Foundations improves the typical ML workflow.

### Machine Learning Workflow and Challenges

Machine learning is experimental - having to gather and pre-process different datasets, test and optimize different models, and run code without knowing the final result provides different challenges from traditional software development. Because of this, 

* Keeping track of results is hard - When running hundreds of experiments to optimize 
* Reproducing experiments is difficult - 
* Deploying your model - t




### The Typical Machine Learning Workflow

When developing a machine learning model for production, typically the workflow is as follows

* Development of the model code: Foundations provides SDK functions to add to your code which allow you
* Optimizing your model code: By deploying your code with Foundations via Foundations jobs, you can launch hundreds of experiment simultaneously
* Deploying the best model: 


All code run through Foundations is stored within the platform, so that users can retrieve 
A standard interface with your code can bundle 

Writing your code, optimizing the model, serving it

### Foundations Jobs

A job in Foundations is a unit of work created when the user runs some machine learning code through Foundations. A job can be **deployed** with Foundations via the CLI or SDK, and Foundations runs the deployed code and dependencies in the same expected manner as running a script with `python`, but gets tracked and logged with Foundations. 

Jobs run in an execution environment that can be local or remote. When a job is deployed, a job object is created and deployed to the execution environment where it's picked up by Foundations' scheduler which is in charge of controlling it, tracking it and providing useful information about it to the user.

