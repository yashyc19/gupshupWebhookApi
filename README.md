# Gupshup Webhook API

A Python-based microservice exposing both REST API endpoints and webhook endpoints for handling and storing OTP messages. This service receives webhook data from external services like Gupshup, processes and filters messages containing OTP information, and provides REST API endpoints to retrieve and manage the stored messages.

## Features

- **Webhook Receiver**: Receives and processes webhook data from external services
- **Message Filtering**: Only stores messages containing OTP (One-Time Password) information
- **REST API**: Endpoints to retrieve and manage stored messages
- **File-based Storage**: Persists data in JSON files (easily extensible to databases)
- **Environment Configuration**: Supports multiple environments (dev/qa/prod)
- **Docker Support**: Containerized application with Docker and Docker Compose
- **Health Checks**: Endpoint for monitoring application status

## API Endpoints

### Webhook Endpoints

- **POST `/webhook/{source}/{phone}`**: Receive webhook data
  - **Parameters**:
    - `source`: Source of the webhook (e.g., 'gupshup', 'twilio')
    - `phone`: Phone number associated with the message
  - **Status Codes**:
    - `201`: Message stored successfully (contains OTP)
    - `200`: Message received but not stored (no OTP)
    - `400`: Validation errors in request

### REST API Endpoints

- **GET `/api/{source}/{phone}`**: Get all messages for a source and phone
  - **Parameters**:
    - `source`: Source of the messages (e.g., 'gupshup')
    - `phone`: Phone number associated with the messages
  - **Status Codes**:
    - `200`: Success
    - `400`: Invalid parameters

- **GET `/api/{source}/{phone}/{message_id}`**: Get a specific message
  - **Parameters**:
    - `source`: Source of the message
    - `phone`: Phone number associated with the message
    - `message_id`: ID (timestamp) of the message
  - **Status Codes**:
    - `200`: Success
    - `404`: Message not found
    - `400`: Invalid parameters

- **DELETE `/api/{source}/{phone}/{message_id}`**: Delete a specific message
  - **Parameters**:
    - `source`: Source of the message
    - `phone`: Phone number associated with the message
    - `message_id`: ID (timestamp) of the message
  - **Status Codes**:
    - `200`: Message deleted successfully
    - `404`: Message not found
    - `400`: Invalid parameters

- **DELETE `/api/{source}/{phone}/delete_all`**: Delete all messages for a source and phone
  - **Parameters**:
    - `source`: Source of the messages
    - `phone`: Phone number associated with the messages
  - **Status Codes**:
    - `200`: All messages deleted successfully
    - `500`: Failed to delete messages
    - `400`: Invalid parameters

- **DELETE `/api/delete_all_data`**: Delete all webhook data across all sources and phone numbers
  - **Status Codes**:
    - `200`: All data deleted successfully or no data to delete
    - `207`: Some files could not be cleared

- **GET `/health`**: Health check endpoint
  - **Status Codes**:
    - `200`: Application is running

## Installation and Setup

### Prerequisites

- Python 3.8+
- Docker (optional, for containerized deployment)

### Local Development

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/gupshup-webhook-api.git
   cd gupshup-webhook-api
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Set up environment variables (create a `.env` file):
   ```
   ENV=dev
   PORT=8000
   HOST=0.0.0.0
   DATA_DIR=data
   ```

4. Run the application:
   ```bash
   python -m src.app
   ```

### Docker Deployment

1. Build and run with Docker Compose:
   ```bash
   docker-compose up -d
   ```

2. For production, use environment-specific settings:
   ```bash
   ENV_NAME=prod docker-compose up -d
   ```

## Project Structure

```
gupshup-webhook-api/
├── data/                         # Data storage directory
├── src/                          # Application source code
│   ├── api/                      # API endpoints
│   ├── config/                   # Configuration management
│   ├── persistence/              # Data persistence layer
│   ├── webhook/                  # Webhook handling
│   └── app.py                    # Application entry point
├── tests/                        # Test files
├── Dockerfile                    # Docker configuration
├── docker-compose.yml            # Docker Compose configuration
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## Configuration

The application uses environment variables for configuration:

- `ENV`: Environment (dev/qa/prod)
- `PORT`: Port for the server (default: 8000)
- `HOST`: Host to bind the server (default: 0.0.0.0)
- `DATA_DIR`: Directory for JSON file storage (default: data)

## Testing

Run tests using pytest:

```bash
pytest
```

## Docker Health Check

The application includes a health check endpoint at `/health` that Docker uses to monitor the container's health status.

