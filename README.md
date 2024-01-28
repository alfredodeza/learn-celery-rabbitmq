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
  . main.async_parse_exploits
  . main.async_send_email
```

## Start Flask

Start the Flask application with the following command:

```bash
flask --app app.main:flask_app run --reload
```

This will load the Flask application on port 5000 by default. Verify it is running by opening a browser and going to [http://localhost:5000](http://localhost:5000).

Try a different port if you are running into a port conflict:

```bash
flask --app app.main:flask_app run --reload -p 5001
```

## Send a request for async processing

Create a new `POST` request to the running application to the `/send_email` endpoint. You can use the following `curl` command:

```bash
curl -X POST --header "Content-Type: application/json" --data '{"email": "john.doe@example.org", "subject": "hi from Celery!", "body": "Just a test"}' http://localhost:5001/send_email
```

This request will not return any values and it mimics a "fire and forget" type of processing. The request will be sent to the Flask application, which will then send the request to Celery for processing. Celery will then send the request to RabbitMQ for processing. RabbitMQ will then send the request to a Celery worker for processing. The Celery worker will then process the request and send the email.

## Send a request for async processing with a response

Create a new `POST` request to the running application to the `/parse_exploits` endpoint. You can use the following `curl` command:

```bash
curl -X POST http://localhost:5000/parse_exploits
```

You will get a response that looks like the following:

```json
{
    "task_id": 1
}
```

You can then use the `task_id` to query the status of the task to see if it is complete. You can use the following `curl` command that will request the information to the endpoint `/check_task/<task_id>`:

```bash
curl -X GET http://localhost:5000/check_task/1
```

You will get a response that looks like the following:

```json
{
        "task_id": 1, 
        "task_status": "PENDING", 
        "task_result": [[CVE-2019-1622, CVE-2019-1623, CVE-2019-1624, CVE-2019-1625, CVE-2019-1626, CVE-2019-1627, CVE-2019-1628, CVE-2019-1629, CVE-2019-1630, CVE-2019-1631, CVE-2019-1632, CVE]]
}
```
