from flask_restful import Resource
from flask import request, jsonify
import config
import os
import json
# from util.customLogger import LogGen

# Set up logging
# gupshup_logger = LogGen.loggen('gupshup')

# Standard output message
STD_OUTPUT = {
    'status': 'success',
    'message': 'This is a Gupshup webhook',
}

class GupshupWebhook(Resource):
    """
    A Flask-RESTful resource for handling Gupshup webhooks.
    """

    # def get(self):
    #     """
    #     Handle GET requests and return a standard output message.
    #     """
    #     output = STD_OUTPUT.copy()
    #     output['message'] = 'Listening for incoming messages'
    #     # gupshup_logger.info('GET request received')
    #     return jsonify(output)

    def get(self, phno=None):
        """
        Get sms data from Gupshup API, save it to a file, and return a standard output message.
        """
        webhookdata = request.args
        if not any(webhookdata.values()):
            output = STD_OUTPUT.copy()
            output['status'] = 'error'
            output['message'] = 'No data provided'
            return output, 400
        
        datapath = f'{phno}_{config.WEBHOOK_DATA_FILE}' if phno else config.WEBHOOK_DATA_FILE
        # os.makedirs(os.path.dirname(datapath), exist_ok=True)
        try:
            if not os.path.exists(datapath):
                with open(datapath, 'a') as f:
                    json.dump([], f)
    
            with open(datapath, 'r') as f:
                data = json.load(f)
            
            content = webhookdata.get('content')
            # print(content)
            if 'OTP' in content or 'otp' in content or 'One Time Password' in content:  # check if the message contains OTP
                data.append(webhookdata)
                with open(datapath, 'w') as f:
                    json.dump(data, f)
                output = STD_OUTPUT.copy()
                output['message'] = 'Data saved to file - OTP message'
                return output, 201
            else:
                print(f"Data received but not saved: {webhookdata}")
                output = STD_OUTPUT.copy()
                output['message'] = 'Data received but not saved'
                return output, 200
    
        except Exception as e:
            print(e)
            output = STD_OUTPUT.copy()
            output['status'] = 'error'
            output['message'] = 'Error saving data to file'
            return output, 500

# ----------------------------

class GupshupAPI(Resource):
    """
    A Flask-RESTful resource for handling Gupshup API requests.
    """
    # TODO: Implement this class
    STD_OUTPUT = {
        'status': 'success',
        'message': 'This is a Gupshup API',
    }

    # get method for the Gupshup API
    # this get method will either recv request like /gupshup/api or /gupshup/api/<messageid>
    # if the request is /gupshup/api then it will return, the whole data saved in the file
    # if the request is /gupshup/api/<messageid> then it will return the data of that particular messageid
    def get(self,phno=None, message_id=None):
        """
        Get sms data from Gupshup API data file and return it.

        If message_id is provided, return the data of that particular message_id.
        """
        # Log the POST request
        # gupshup_logger.log_request(request)
        # get the query parameters

        datapath = f'{phno}_{config.WEBHOOK_DATA_FILE}' if phno else config.WEBHOOK_DATA_FILE
        # if file does not exist then return no data found
        if not os.path.exists(datapath):
            output = STD_OUTPUT.copy()
            output['message'] = 'No data file found'
            return output, 404
        
        # read the file
        with open(datapath, 'r') as f:
            data = json.load(f)

        # if messageid is not provided then return the whole data
        if message_id is None:
            output = STD_OUTPUT.copy()
            # message will be 'Data found' if data is present else 'No data at the moment' if the data is empty
            output['message'] = 'Data found' if data else 'No data at the moment'
            output['data'] = data
            return output, 200
        else:
            # if messageid is provided then return the data of that particular messageid
            for d in reversed(data):
                if 'Time' in d and d['Time'] == message_id:
                    output = STD_OUTPUT.copy()
                    output['message'] = 'Data found'
                    output['data'] = d
                    return output, 200
            output = STD_OUTPUT.copy()
            output['message'] = 'No data found'
            return output, 404
        
    # delete method for the Gupshup API
    # this delete method will delete the data with respect to message_id saved in the file
    def delete(self, phno=None, message_id=None):
        """
        Delete sms data from Gupshup API data file and return a standard output message.
        """
        # Log the POST request
        # gupshup_logger.log_request(request)
        # get the query parameters

        if message_id is None:
            output = STD_OUTPUT.copy()
            output['status'] = 'error'
            output['message'] = 'No message_id provided'
            return output, 400

        datapath = f'{phno}_{config.WEBHOOK_DATA_FILE}' if phno else config.WEBHOOK_DATA_FILE
        # if file does not exist then return no data found
        if not os.path.exists(datapath):
            output = STD_OUTPUT.copy()
            output['message'] = 'No data file found'
            return output, 404
        
        # read the file
        with open(datapath, 'r') as f:
            data = json.load(f)
        
        # delete the data with respect to message_id
        for d in reversed(data):
            print(d)
            if 'Time' in d and d['Time'] == message_id:
                data.remove(d)
                break
        
        # write the data back to the file
        with open(datapath, 'w') as f:
            json.dump(data, f)
        
        output = STD_OUTPUT.copy()
        output['message'] = 'Data deleted'
        return output, 200