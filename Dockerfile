# Use a slim Python image
FROM python:3.9-slim

WORKDIR /app

# Install dependencies
RUN pip install flask prometheus_client

# Install netstat (via net-tools)
RUN apt-get update && apt-get install -y \
    net-tools curl telnet \
    && rm -rf /var/lib/apt/lists/*

# Copy the application code
COPY app2.py .

# Expose the Flask port
EXPOSE 5000

CMD ["python", "app2.py"]
