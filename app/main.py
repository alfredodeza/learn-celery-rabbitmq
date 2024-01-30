from celery import Celery, Task, shared_task
from celery.result import AsyncResult
from flask import Flask, request
import requests
from bs4 import BeautifulSoup 


def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app

def create_app() -> Flask:
    app = Flask("flask-queue")
    app.config.from_mapping(
        CELERY=dict(
            broker="amqp://localhost:5672",
            result_backend='rpc',
        ),
    )
    app.config.from_prefixed_env()
    celery_init_app(app)
    return app

flask_app = create_app()
celery_app = flask_app.extensions["celery"]


@flask_app.get("/")
def root():
    return """<html>
    <h2>A Flask app with Celery and RabbitMQ</h2>
    <p>You can POST to the following endpoint to simulate sending an email asynchronously</p>
    <em>curl -X POST --header "Content-Type: application/json" --data '{"email": "john.doe@example.org", "subject": "hi from Celery!", "body": "Just a test"}' http://localhost:5000/send_email</em>
    </html>"""


@flask_app.post("/send_email")
def send_email():
    email = request.json['email']
    subject = request.json['subject']
    body = request.json['body']
    async_send_email.delay(email, subject, body)
    return {}

@shared_task()
def async_send_email(email, subject, body):
    # simulate a very costly operation of sending an email for 5 seconds
    from time import sleep
    sleep(5)
    return {"success": True, "email": email, "subject": subject, "body": body}

@flask_app.post("/parse_exploits")
def parse_exploits():
    # call the parse exploits function asynchronously
    result = async_parse_exploits.delay()
    # return the id of the task
    return {"task_id": result.id}


@shared_task()
def async_parse_exploits():
    response = requests.get("https://cve.mitre.org/data/refs/refmap/source-EXPLOIT-DB.html")
    soup = BeautifulSoup(response.content, 'html.parser')

    table = None
    count = 0
    
    for child in soup.find_all('table'):
        if len(child.find_all('tr')) > 100:
            table = child

    for row in table.find_all('tr'):
        if count > 100: 
            break

        exploits = []
        try:
            # Get first td text 
            exploit_id = row.find('td').text 
            
            # Get third td text
            cve_id = row.find_all('td')[1].text.strip()
            
            print(f"exploit id: {exploit_id} -> {cve_id}")
            exploits.append([exploit_id, cve_id])
        
        except Exception as err:
            print(f"skipping due to: {err}")

        return exploits

@flask_app.get("/check_task/<task_id>")
def check_task(task_id):
    result = AsyncResult(task_id)
    return {
        "task_id": result.id, 
        "task_status": result.status, 
        "task_result": result.result
    }