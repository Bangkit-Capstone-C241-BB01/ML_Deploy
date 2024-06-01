# ML - Flask for Deployment

To enable it with docker, you can enable it with

```
docker build -t flask_docker_ml .
```

After it succeed, enable it with terminal

```
docker container run -p 5000:5000 flask_docker_ml
```

Afterward, this can be accessed in http://127.0.0.1:5000