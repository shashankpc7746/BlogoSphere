# Gunicorn configuration file
# Increases worker timeout to handle slow SMTP connections

# Bind to the PORT environment variable (Render provides this)
bind = "0.0.0.0:10000"

# Number of worker processes (Render sets WEB_CONCURRENCY automatically)
workers = 1

# Worker timeout in seconds (default is 30, increased for email operations)
timeout = 120

# Keep-alive connections
keepalive = 5

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"
