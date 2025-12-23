from flask import Flask, request, Response
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
import os

app = Flask(__name__)

# 1. Use Environment Variables for Versioning
VERSION = os.getenv("APP_VERSION", "v1.0.0")

# 2. Define Metrics
REQUEST_COUNT = Counter(
    'http_requests_total', 
    'Total HTTP Requests', 
    ['method', 'endpoint', 'version', 'status']
)

# 3. Automatic Tracking Middleware
@app.after_request
def collect_metrics(response):
    # This captures every request automatically
    REQUEST_COUNT.labels(
        method=request.method, 
        endpoint=request.path, 
        version=VERSION,
        status=response.status_code
    ).inc()
    return response

@app.route('/')
def hello():
    return {"message": f"Hello! Running version: {VERSION}"}

# 4. Correct Metrics Endpoint
@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == '__main__':
    # Use threaded=True for better performance in dev
    app.run(host='0.0.0.0', port=5000, threaded=True)
