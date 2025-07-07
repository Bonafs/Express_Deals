web: gunicorn express_deals.wsgi --log-file -
worker: celery -A express_deals worker --loglevel=info
beat: celery -A express_deals beat --loglevel=info
