# schedulr

## Requirements

- Docker
- A reverse proxy

## Build and running

Create an .env file from the .env.example and fill accordingly.

Start the container, feel free to adjust the port (8086) to your liking.

```
docker build --target prod -t schedulr -f Dockerfile .
docker run -d --name schedulr \
  -p 127.0.0.1:8086:8000 \
  --env-file .env \
  -v $(pwd)/data:/usr/app/data \
  --restart always \
  schedulr
```

## Why don't you just have an image I can pull?

Haven't gotten around to it (yet).
