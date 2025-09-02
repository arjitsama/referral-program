# ===============================
# Springer Capital Referral Pipeline
# Dockerfile for containerization
# ===============================

# 1. Use an official Python base image
FROM python:3.10-slim

# 2. Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Set working directory inside the container
WORKDIR /app

# 4. Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Install PySpark separately (sometimes it’s large)
RUN pip install pyspark

# 6. Copy application code into the container
COPY main.py .
COPY data ./data

# 7. Create folders for outputs (mounted later as volumes)
RUN mkdir -p /app/output /app/profiling

# 8. Default command to run the pipeline
CMD ["python", "main.py"]
