FROM python:3.10-slim  # Base image

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Mount Docker volume (optional)
VOLUME ${WEBHOOK_DATA_VOLUME}:/app/data

# Copy project files
COPY . .

# Start the Flask application
CMD ["python", "app/app.py"]  # Replace with your main script if different