import multiprocessing

# Gunicorn configuration file
bind = "0.0.0.0:8000"

# Worker configuration
workers = 2  # Reduce number of workers to save memory
worker_class = "sync"
worker_connections = 1000
timeout = 120  # Increase timeout to 120 seconds
keepalive = 2

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"

# Process naming
proc_name = "image_colorizer"

# Limit worker memory usage
max_requests = 100
max_requests_jitter = 10

# Preload app to save memory
preload_app = True