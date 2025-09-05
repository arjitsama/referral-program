# Springer Capital Referral Pipeline
# Dockerfile for containerization

# 1. Use an official Python base image
FROM python:3.11-slim

# 2. Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Set working directory
WORKDIR /app

# 4. Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. (Optional) Install PySpark if required
# Keep it here so it doesn’t bloat requirements.txt unnecessarily
RUN pip install pyspark

# 6. Copy application code
COPY main.py .

# 7. Create output directories (these will be mounted as volumes at runtime)
RUN mkdir -p /app/output /app/profiling

# 8. Default command
CMD ["python", "main.py", "--input_dir", "/app/data", "--output_dir", "/app/output", "--profile_dir", "/app/profiling"]
