FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY datacomparison_app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY datacomparison_app .

EXPOSE 5000

# Run with Gunicorn in production; 4 workers is a sensible default
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "app:app"]
