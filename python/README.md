# Restb.ai python3 SDK

### Overview

This sub-project contains sample python3 code for accessing Restb.ai's RESTful API service for AI Computer Vision.

### Layout

The primary package for calling our API resides in the `restb.sdk` module. Specifically, `api.service` is how the API
can be invoked. Examples for all of the parameters are outlined in the `__init__.py` file within the `restb.sdk` module.

### Example

There is a runnable example located in the `restb.examples` module, which can be run from the `python` folder as follows:

```
# python3 -m restb.examples.run
```

To make the example function, you need only update it with your `client_key` where it says `YOUR_CLIENT_KEY_HERE` in the `run.py` file.

### Instructions

In order to use the SDK or run the example, you only need to install the required libraries as follows:

```
# pip3 install -r requirements.lock
```
