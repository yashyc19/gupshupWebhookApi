from flask_restful import Api
from flask import Flask
from src.resources.gupshup import GupshupAPI, GupshupWebhook

app = Flask(__name__)
api = Api(app)

# Get sms data from gupshup via webhook endpoint
# Add one more parameter to the endpoint, new /gupshup/<phno>/webhook
api.add_resource(GupshupWebhook, '/gupshup/<string:phno>/webhook')
# api.add_resource(GupshupWebhook, '/gupshup/webhook')

# Get and delete sms data from gupshupapi via API endpoint
# Add one more parameter to the endpoint, new /gupshup/<phno>/api...
api.add_resource(GupshupAPI, '/gupshup/<string:phno>/api', '/gupshup/<string:phno>/api/<string:message_id>')
# api.add_resource(GupshupAPI, '/gupshup/api', '/gupshup/api/<string:message_id>')


if __name__ == '__main__':
    app.run(port=8000, debug=True)
    # app.run(host='0.0.0.0', port=8000, debug=True)