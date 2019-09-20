<h1>Foundations Atlas Features</h1>

This section of documentation is the single source of truth regarding in-depth explanation of the features that you will find within Foundations.

If you are looking for specific API usage, that can be found in [API docs (TODO)]().

## Atlas Paradigm & Submitting Code
The paradigm that Atlas follows can be initially confusing to anyone who hasn't seen it before... But we promise that it makse sense once it clicks!

__The basic concept is this__: With zero changes to your Python code, you can send your code to a remote machine that will run it. With minimal, non-intrusive changes to your code, you should start seeing functional value from Atlas.

#### Job Directory

![Minimal Project Structure](../../../theme/assets/images/minimum_project_structure_1.png "Minimal Project Structure")

Let us assume that the structure of our project, text_generation_simple, looks like the above. This is the *minimum* that we need to run a Python script and is conveniently the minimum that you need to run a Foundations job.

This file, main.py, does not even need any references to Foundations. It could simply be:
```python 
print("Hello, Universe!")
```

If we submit our code using the `foundations deploy` CLI command:
- we will see the 
- a project will appear in the Dashboard [TODO]() with any possible job information being filled out.

## Submitting Code

#### Job Directory

###### Entrypoints

###### Hyperparameter Files

#### Hyperparameter Search

#### Debugging

## The Dashboard

#### Job Information

######

#### Parameters

#### Metrics

## Model Packaging

#### Manifest Files

