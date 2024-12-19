# gunicorn_config.py
timeout = 300  # 5 minutes timeout
workers = 1
threads = 1
worker_class = 'gthread'