FROM python:3.11-slim
RUN pip install --no-cache-dir prometheus-client
WORKDIR /app
COPY metrics.py /app/metrics.py
CMD ["python", "/app/metrics.py"]

