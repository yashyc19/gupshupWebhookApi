# create a dockerfile to build the image

# Use an official Python runtime as a parent image
FROM python:3.11.0-slim
RUN apt-get update
RUN apt update

WORKDIR /usr/gupshupWebhookAPI

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .


# want to run this api on a standard port
EXPOSE 80

# run the command to start the api
ENTRYPOINT [ "python" ]
CMD [ "app.py" ]

