FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better layer caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create volume for data persistence
VOLUME ["/app/data"]

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Set environment variables
ENV PORT=8000
ENV HOST=0.0.0.0
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE 8000

# Run the application with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "src.app:app"]
