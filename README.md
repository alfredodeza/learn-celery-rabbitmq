# Distributed queuing with Flask, Celery, and RabbitMQ

This repository will guide you through examples that you can use to implement
powerful queue patterns using RabbitMQ as the message broker.



## System requirements

This repository is Codespaces ready, so RabbitMQ and the Flask Python
application will work out of the box. If you are learning how these all work
together, it is the **easiest way to get started** without feeling overwhelmed
by the complexity of installing dependencies. 

If you want to use Docker on your own system you can run the following:

```bash
# latest RabbitMQ 3.12
docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.12-management
```

Finally, for other systems, refer to the [download installation documentation on
RabbitMQ's website](https://www.rabbitmq.com/download.html).

## Start Celery

Celery needs to get started. First, make sure RabbitMQ is running by opening a terminal and running:

```
ps aux | grep rabbitmq
```

You should get output that displays the RabbitMQ process.

Start Celery by doing:

```bash
celery -A make_celery worker --loglevel INFO
```

You should see in the output that the `async_send_email` task is registered:

```
[tasks]
  . main.async_send_email
```
