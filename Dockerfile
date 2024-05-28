# create a dockerfile to build the image

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

# Define environment variable for GUNICORN_CMD_ARGS if you need to customize Gunicorn settings
ENV GUNICORN_CMD_ARGS="--bind 0.0.0.0:8000"

# Use an entrypoint script to determine how to run the application
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
CMD ["gunicorn", "-w", "4", "app:app"]


# ------------------------------------
# for development - use the following entrypoint.sh
# #!/bin/sh

# if [ -n "$GUNICORN_CMD_ARGS" ]; then
#     exec gunicorn "$@"
# else
#     exec python app.py
# fi
# ------------------------------------

# for dev - docker run -p 5000:8000 your-image-name
# for prod - docker run -p 8000:8000 -e GUNICORN_CMD_ARGS="--workers 3 --timeout 0" <image_name>
# (this above command will tell to run with env var)

# Note: for development, you can use the same
#       and for production, you will define the GUNICORN_CMD_ARGS
#       in the env variables
# ------------------------------------