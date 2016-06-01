CELERY_IMPORTS = ('tasks')
CELERY_IGNORE_RESULT = False
BROKER_HOST = "192.168.1.28" # IP address of the server running RabbitMQ and Celery
BROKER_PORT = 5672
BROKER_URL ='amqp://'
CELERY_RESULT_BACKEND = "amqp"
CELERY_IMPORTS = ("tasks",)