# Distributed queuing with Flask, Celery, and RabbitMQ

This repository will guide you through examples that you can use to implement
powerful queue patterns using RabbitMQ as the message broker.


## System requirements

This repository requires system-level dependencies so that RabbitMQ can get
started.

If you want to use Docker on your own system you can run the following:

```bash
# latest RabbitMQ 3.12
docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.12-management
```


For other systems, refer to the [download installation documentation on
RabbitMQ's website](https://www.rabbitmq.com/download.html).


This repository is Codespaces ready, so RabbitMQ and the Flask Python
application will work out of the box. If you are learning how these all work
together, it is the **easiest way to get started** without feeling overwhelmed
by the complexity of installing dependencies. 


