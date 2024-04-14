from flask_restful import Api
from flask import Flask
from app.resources.gupshup import GupshupWebhook, GupshupAPI

app = Flask(__name__)
api = Api(app)

# Get sms data from gupshup via webhook endpoint
api.add_resource(GupshupWebhook, '/gupshup/webhook')
# Get and delete sms data from gupshupapi via API endpoint
api.add_resource(GupshupAPI, '/gupshup/api', '/gupshup/api/<string:message_id>')