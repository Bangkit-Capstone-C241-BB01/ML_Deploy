# ML - Flask for Deployment

To enable it with docker, you can enable it with

```
docker build -t flask_docker_ml .
```

After it succeed, enable it with terminal.
Replace [any port] with other port other than 5000

```
docker container run -p [any port]:5000 flask_docker_ml
```

Afterward, this can be accessed in your local http://127.0.0.1:[any port]
