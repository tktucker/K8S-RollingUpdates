from flask import Flask
from prometheus_client import start_http_server, Counter, generate_latest

app = Flask(__name__)

# Define a Prometheus Counter
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP Requests', ['method', 'endpoint', 'version'])

VERSION = "v3.0.0"  # Update this to "v2.0.0" for your second image

@app.route('/')
def hello():
    # Increment the counter
    REQUEST_COUNT.labels(method='GET', endpoint='/', version=VERSION).inc()
    return f"Hello! This is v1 Running version: {VERSION}"

@app.route('/metrics')
def metrics():
    # Expose the metrics to Prometheus
    return generate_latest()

if __name__ == '__main__':
    # Start Prometheus metrics server on port 8000
    # Note: You can also just use the /metrics route above
    app.run(host='0.0.0.0', port=5000)
