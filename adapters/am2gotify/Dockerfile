FROM python:3.11-alpine
RUN pip install --no-cache-dir flask requests gunicorn
WORKDIR /app
COPY app.py /app/app.py
CMD ["gunicorn","-b","0.0.0.0:5000","app:app"]
