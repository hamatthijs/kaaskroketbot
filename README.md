# Docker start - Discord bot

## How to start

Build the image:

```shell
docker build -t name-of-image path/to/dockerfile
```

Run the bot:

```shell
docker run -d --name name-of-container -v /var/run/docker.sock:/var/run/docker.sock --restart unless-stopped name-of-image
```
