"""
API Module

This module provides REST API endpoints for retrieving and managing webhook messages.
The API allows clients to retrieve all messages for a specific source and phone number,
get individual messages by their ID, and delete messages when they are no longer needed.

Routes:
    GET /api/<source>/<phone>: Get all messages for a source and phone number
    GET /api/<source>/<phone>/<message_id>: Get a specific message by ID
    DELETE /api/<source>/<phone>/<message_id>: Delete a specific message by ID
"""

from typing import Dict, Any, Tuple
from flask import jsonify, request, Blueprint

from src.persistence.json_store import JsonFilePersistence

# Create a Flask blueprint for API routes with prefix '/api'
# eg: /api/gupshup/1234567890
# This allows for better organization of routes and separation of concerns
api_bp = Blueprint('api', __name__, url_prefix='/api')

# Initialize the persistence layer
# This is where the webhook messages will be stored
# The JsonFilePersistence class handles the file-based storage of messages
# Each source and phone number combination will have its own JSON file
# The data_dir is set to the DATA_DIR from the Config class
# This allows for easy configuration and management of the storage location
# The JsonFilePersistence class is responsible for saving, retrieving, and deleting messages
store = JsonFilePersistence()

@api_bp.route('/<source>/<phone>', methods=['GET'])
def get_all_messages(source: str, phone: str) -> Tuple[Dict[str, Any], int]:
    """
    Get all messages for a specific source and phone number.
    
    This endpoint retrieves all stored webhook messages for a specific
    source (e.g., 'gupshup') and phone number combination.
    
    Args:
        source (str): The source of the webhook (e.g., 'gupshup', 'twilio')
        phone (str): The phone number associated with the webhook messages
    
    Returns:
        Tuple[Dict[str, Any], int]: A tuple containing:
            - A JSON object with message IDs as keys and message data as values
            - HTTP status code 200 (OK)
            
    Response Format:
        {
            "2023-04-22T10:00:00Z": {
                "content": "Your OTP code is 123456",
                "timestamp": "2023-04-22T10:00:00Z"
            },
            "2023-04-22T11:00:00Z": {
                "content": "Your verification code is 654321",
                "timestamp": "2023-04-22T11:00:00Z"
            }
        }
            
    Example:
        GET /api/gupshup/1234567890
    """
    messages = store.get_messages(source, phone)
    return jsonify(messages), 200

@api_bp.route('/<source>/<phone>/<message_id>', methods=['GET'])
def get_message(source: str, phone: str, message_id: str) -> Tuple[Dict[str, Any], int]:
    """
    Get a specific message by ID for a source and phone number.
    
    This endpoint retrieves a single webhook message identified by its
    message ID (timestamp) for a specific source and phone number.
    
    Args:
        source (str): The source of the webhook (e.g., 'gupshup', 'twilio')
        phone (str): The phone number associated with the webhook message
        message_id (str): The ID (timestamp) of the message to retrieve
    
    Returns:
        Tuple[Dict[str, Any], int]: A tuple containing:
            - If message exists: The message data and HTTP status 200 (OK)
            - If message not found: Error message and HTTP status 404 (Not Found)
            
    Response Format (success):
        {
            "content": "Your OTP code is 123456",
            "timestamp": "2023-04-22T10:00:00Z"
        }
        
    Response Format (error):
        {
            "error": "Message not found"
        }
            
    Example:
        GET /api/gupshup/1234567890/2023-04-22T10:00:00Z
    """
    message = store.get_message(source, phone, message_id)
    if not message:
        return jsonify({"error": "Message not found"}), 404
    return jsonify(message), 200

@api_bp.route('/<source>/<phone>/<message_id>', methods=['DELETE'])
def delete_message(source: str, phone: str, message_id: str) -> Tuple[Dict[str, Any], int]:
    """
    Delete a specific message by ID for a source and phone number.
    
    This endpoint removes a single webhook message identified by its
    message ID (timestamp) for a specific source and phone number.
    
    Args:
        source (str): The source of the webhook (e.g., 'gupshup', 'twilio')
        phone (str): The phone number associated with the webhook message
        message_id (str): The ID (timestamp) of the message to delete
    
    Returns:
        Tuple[Dict[str, Any], int]: A tuple containing:
            - If deletion successful: Success message and HTTP status 200 (OK)
            - If message not found: Error message and HTTP status 404 (Not Found)
            
    Response Format (success):
        {
            "message": "Message deleted successfully"
        }
        
    Response Format (error):
        {
            "error": "Message not found"
        }
            
    Example:
        DELETE /api/gupshup/1234567890/2023-04-22T10:00:00Z
    """
    success = store.delete_message(source, phone, message_id)
    if not success:
        return jsonify({"error": "Message not found"}), 404
    return jsonify({"message": "Message deleted successfully"}), 200
