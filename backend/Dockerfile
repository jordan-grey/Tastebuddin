# Use a lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy dependency file and install first (cache-friendly)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend files (app.py, recipe_service.py, etc.)
COPY . .

# Environment setup
ENV PYTHONUNBUFFERED=1 \
    FLASK_APP=app.py \
    FLASK_RUN_HOST=0.0.0.0 \
    FLASK_RUN_PORT=5000 \
    FLASK_ENV=development

# Expose port
EXPOSE 5000

# Run Flask
CMD ["python", "-m", "flask", "run"]
