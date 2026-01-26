# gunicorn.conf.py
import multiprocessing

# Bind e workers
bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count() * 2 + 1
threads = 2
worker_class = "sync"
worker_connections = 1000
backlog = 2048

# Tempo de execução
timeout = 30
graceful_timeout = 30
keepalive = 2
max_requests = 1000
max_requests_jitter = 100
preload_app = True

# Logs
accesslog = "-"
errorlog = "-"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Segurança
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# Melhor desempenho (uso de memória RAM para tmp dos workers)
worker_tmp_dir = "/dev/shm"

# Proxy headers (NGINX → Gunicorn)
forwarded_allow_ips = "*"
proxy_allow_ips = "*"
secure_scheme_headers = {
    "X-FORWARDED-PROTO": "https",
    "X-FORWARDED-SSL": "on",
}

# Desativa reload (produção)
reload = False
