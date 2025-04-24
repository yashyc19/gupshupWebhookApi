"""
Webhook Routes Module

This module handles incoming webhook requests from external services like Gupshup.
It provides endpoints for receiving webhook data, validating payloads,
and determining whether to store messages based on content filtering criteria.

Routes:
    POST /webhook/<source>/<phone>: Receive and process webhook data from a specific source for a specific phone number
"""

from typing import Dict, Any, Tuple
from flask import jsonify, request, Blueprint
from datetime import datetime

from src.persistence.json_store import JsonFilePersistence
from src.webhook import process_webhook

# Create a Flask blueprint for webhook routes with prefix '/webhook'
webhook_bp = Blueprint('webhook', __name__, url_prefix='/webhook')

# Initialize the persistence layer
store = JsonFilePersistence()

@webhook_bp.route('/<source>/<phone>', methods=['POST'])
def receive_webhook(source: str, phone: str) -> Tuple[Dict[str, Any], int]:
    """
    Receive and process webhook data from external services.
    
    This endpoint validates incoming webhook query parameters, processes them through
    the webhook processing pipeline, and conditionally stores messages that
    contain OTP or verification content.
    
    Args:
        source (str): The source of the webhook (e.g., 'gupshup', 'twilio')
        phone (str): The phone number associated with the webhook message
    
    Returns:
        Tuple[Dict[str, Any], int]: A tuple containing a JSON response and HTTP status code:
        - 201 if message was stored successfully (contains OTP)
        - 200 if message was received but not stored (no OTP)
        - 400 if there were validation errors in the request
        - 500 if there was a server error processing the request
    
    Query Parameters:
        content: The message text content (required)
        timestamp: The timestamp of the message (optional, will be generated if not provided)
        Additional parameters will be stored alongside the message
        
    Example:
        POST /webhook/gupshup/1234567890?content=Your%20OTP%20code%20is%20123456&timestamp=1725014964572
    """
    try:
        # Step 1: Get data from query parameters
        data = dict(request.args)
        
        # Step 2: Validate that we have query parameters
        if not data:
            return jsonify({"error": "Request must have query parameters"}), 400
        
        # Step 3: Check that required fields are present in the parameters
        if "content" not in data:
            return jsonify({"error": "Missing required parameter: content"}), 400
            
        # Step 4: Ensure message has a timestamp
        if 'timestamp' not in data:
            data['timestamp'] = str(int(datetime.utcnow().timestamp() * 1000))  # Use milliseconds timestamp format
            
        # Step 5: Process the webhook message through our filtering logic
        # This determines if the message contains OTP or verification content
        should_store = process_webhook(source, phone, data)
        
        if should_store:
            # Store the message
            message_id = store.save_message(source, phone, data)
            return jsonify({"message": "Webhook processed and stored", "message_id": message_id}), 201
        else:
            # Message received but not stored (no OTP)
            return jsonify({"message": "Webhook received but not stored"}), 200
            
    except Exception as e:
        # In a real app, use proper logging
        print(f"Error processing webhook: {str(e)}")
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500
