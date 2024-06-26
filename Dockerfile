# Use an official Python runtime as a parent image
FROM python:3.9.7-slim

# Set the working directory in the container
WORKDIR /usr/gupshupWebhookAPI

# Copy the current directory contents into the container at /usr/gupshupWebhookAPI
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8000 for the app
EXPOSE 8000

# Run the application:
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]