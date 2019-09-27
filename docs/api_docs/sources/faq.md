# FAQ

### 1. Docker credentials error during installation on OSX/Windows
The Atlas CE installer pulls docker images from Google Container Registry during installation.
This can cause the following error on some OSX systems depending on your docker setup:
`docker.credentials.error.InitializationError: docker-credential-desktop not installed or not available in PATH`

A workaround for this error is to remove the `credsStore` tag in your `~/.docker/config.json`


### 1. Docker Engine Timeout
The Docker Engine can timeout at times if multiple quick running jobs are being run or during download of an image with the following error:
`UnixHTTPConnectionPool(host='localhost', port=None): Read timed out. (read timeout=60)`

This can be addressed by increasing the CPU and RAM allocation to the Docker Engine by navigating to the `Advanced` section in Docker settings/preferences depending on your OS.


 



