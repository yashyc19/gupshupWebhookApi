"""
JSON File Persistence Module

This module provides a persistence layer that stores webhook data in JSON files.
Each file corresponds to a unique combination of source and phone number,
with individual messages identified by their timestamps.

The persistence layer handles:
- Saving new webhook messages to appropriate JSON files
- Retrieving messages by source, phone number, and message ID
- Deleting messages when they are no longer needed

This implementation provides a simple file-based storage solution that can be 
replaced with a database solution (MongoDB, PostgreSQL, etc.) in the future.
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any

from src.config import Config


class JsonFilePersistence:
    """
    A persistence layer that stores webhook data in JSON files.
    
    Each file corresponds to a unique source and phone number combination.
    Within each file, messages are stored with their timestamps as keys.
    
    Attributes:
        data_dir (str): Directory where JSON files will be stored
    """
    
    def __init__(self, data_dir: str = None):
        """
        Initialize the JSON file persistence layer.
        
        Args:
            data_dir (str, optional): Directory where JSON files will be stored.
                Defaults to the DATA_DIR from Config if not provided.
        """
        self.data_dir = data_dir or Config.DATA_DIR
        # Create the data directory if it doesn't exist
        os.makedirs(self.data_dir, exist_ok=True)
    
    def _get_file_path(self, source: str, phone: str) -> str:
        """
        Generate the file path for a specific source and phone number.
        
        This private method constructs the full path to the JSON file
        where messages for a specific source and phone will be stored.
        
        Args:
            source (str): The source of the webhook (e.g., 'gupshup', 'twilio')
            phone (str): The phone number associated with the webhook
            
        Returns:
            str: The full file path to the JSON storage file
            
        Example:
            >>> persistence = JsonFilePersistence('/data')
            >>> persistence._get_file_path('gupshup', '1234567890')
            '/data/gupshup_1234567890_webhook_data.json'
        """
        return os.path.join(self.data_dir, f'{source}_{phone}_webhook_data.json')
    
    def save_message(self, source: str, phone: str, message: Dict[str, Any]) -> str:
        """
        Save a webhook message to the appropriate JSON file.
        
        This method adds a timestamp if one isn't present, then stores
        the message in the JSON file corresponding to the source and phone number.
        
        Args:
            source (str): The source of the webhook (e.g., 'gupshup', 'twilio')
            phone (str): The phone number associated with the webhook
            message (Dict[str, Any]): The webhook message data to save
            
        Returns:
            str: The message ID (timestamp) that can be used to retrieve the message
            
        Raises:
            Exception: If there's an error saving the message to the file
            
        Example:
            >>> persistence = JsonFilePersistence()
            >>> message_id = persistence.save_message('gupshup', '1234567890', 
            ...     {'content': 'Your OTP is 123456'})
        """
        file_path = self._get_file_path(source, phone)
        
        # # Ensure message has a timestamp
        # if 'timestamp' not in message:
        #     message['timestamp'] = datetime.utcnow().isoformat()
        
        message_id = message['timestamp']
        
        try:
            # Read existing data
            if os.path.exists(file_path):
                with open(file_path, 'r') as file:
                    data = json.load(file)
            else:
                data = {}
            
            # Add new message
            data[message_id] = message
            
            # Write back to file
            with open(file_path, 'w') as file:
                json.dump(data, file, indent=2)
            
            return message_id
        except Exception as e:
            # In a real app, use proper logging
            print(f'Error saving message: {str(e)}')
            raise
    
    def get_messages(self, source: str, phone: str) -> Dict[str, Any]:
        """
        Get all messages for a specific source and phone number.
        
        Args:
            source (str): The source of the webhook (e.g., 'gupshup', 'twilio')
            phone (str): The phone number associated with the webhook
            
        Returns:
            Dict[str, Any]: A dictionary of all messages for the source and phone,
                with message IDs (timestamps) as keys
                
        Example:
            >>> persistence = JsonFilePersistence()
            >>> messages = persistence.get_messages('gupshup', '1234567890')
            >>> # Returns: {'2023-04-22T10:00:00Z': {'content': 'Your OTP is 123456', ...}}
        """
        file_path = self._get_file_path(source, phone)
        
        if not os.path.exists(file_path):
            return {}
            
        try:
            with open(file_path, 'r') as file:
                return json.load(file)
        except Exception as e:
            # In a real app, use proper logging
            print(f'Error reading messages: {str(e)}')
            return {}
    
    def get_message(self, source: str, phone: str, message_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific message by ID for a source and phone number.
        
        Args:
            source (str): The source of the webhook (e.g., 'gupshup', 'twilio')
            phone (str): The phone number associated with the webhook
            message_id (str): The ID (timestamp) of the message to retrieve
            
        Returns:
            Optional[Dict[str, Any]]: The message if found, None otherwise
            
        Example:
            >>> persistence = JsonFilePersistence()
            >>> message = persistence.get_message('gupshup', '1234567890', '2023-04-22T10:00:00Z')
        """
        messages = self.get_messages(source, phone)
        return messages.get(message_id)
    
    def delete_message(self, source: str, phone: str, message_id: str) -> bool:
        """
        Delete a specific message by ID for a source and phone number.
        
        Args:
            source (str): The source of the webhook (e.g., 'gupshup', 'twilio')
            phone (str): The phone number associated with the webhook
            message_id (str): The ID (timestamp) of the message to delete
            
        Returns:
            bool: True if the message was deleted, False if it wasn't found
            
        Example:
            >>> persistence = JsonFilePersistence()
            >>> success = persistence.delete_message('gupshup', '1234567890', '2023-04-22T10:00:00Z')
            >>> print(success)  # True if deletion was successful
        """
        file_path = self._get_file_path(source, phone)
        
        if not os.path.exists(file_path):
            return False
            
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
            
            if message_id not in data:
                return False
            
            # Remove the message
            del data[message_id]
            
            # Write back to file
            with open(file_path, 'w') as file:
                json.dump(data, file, indent=2)
            
            return True
        except Exception as e:
            # In a real app, use proper logging
            print(f'Error deleting message: {str(e)}')
            return False
