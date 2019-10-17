## Atlas Support & Community

Join our community {==[Slack](https://join.slack.com/t/dessa-community/shared_invite/enQtNzY5ODkxOTc3OTkwLTk4MTg5NmNkOTQ5OWVjNjk2YzY0OWJlNDkwNDlhY2NmNTQzNmRmYjkxNzc2N2JiOTYxZGVkMmFiMjRhYThiYzM)==}
, where you can interact and chat with other Atlas users and Dessa machine learning engineers.
We also periodically post things that we find super interesting 😀.

Alternatively, if you need to get in touch with us shoot us an email at {==[foundations@dessa.com](mailto:foundations@dessa.com)==}

## Known Issues

### Docker issues when launching a job

This issue can manifest itself at a few different times throughout usage, but always comes with a similar error.

For example: if you have logged in using the gcloud library you may see an error like the following when submitting a job.

```bash
docker-credential-gcr not installed or not available in PATH
```

This is **not** an issue with Atlas, but one with Docker. Specifically, it is a problem with how Docker has recently started storing credentials and how it interacts with Docker-in-a-Docker.

**A temporary fix** is to rename, clear, or update `~/.docker/config.json` and restart `atlas-server`. We will update these documents with a supported Docker fix if/when one comes out.