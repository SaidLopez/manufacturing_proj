web: gunicorn core.wsgi --log-file=- 
worker: celery -A core --beat --pool=solo 