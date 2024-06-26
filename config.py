import os


# Docker volume configuration (optional, customize paths)
WEBHOOK_DATA_VOLUME = os.path.join(os.getcwd(), 'data')
WEBHOOK_DATA_FILE = 'webhook_data.json'
