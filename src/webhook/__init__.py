"""
Webhook Processing Module

This module contains the core business logic for processing webhook messages.
It includes functions to analyze message content, detect OTP/verification codes,
and determine whether messages should be stored in the persistence layer.

The primary purpose of this module is to filter incoming messages and only 
store those containing one-time passwords (OTPs) or verification codes.
"""

from typing import Dict, Any, Optional


def contains_otp_keywords(message: Dict[str, Any]) -> bool:
    """
    Check if a message contains OTP-related keywords.
    
    This function analyzes the content of a message to determine if it 
    likely contains a one-time password or verification code.
    
    Args:
        message (Dict[str, Any]): The webhook message to analyze
            Expected to have a 'content' key with string message text
            
    Returns:
        bool: True if the message contains OTP-related keywords, False otherwise
        
    Examples:
        >>> contains_otp_keywords({"content": "Your OTP is 123456"})
        True
        >>> contains_otp_keywords({"content": "Hello, how are you?"})
        False
    """
    if not message or "content" not in message:
        return False
        
    content = message["content"].lower()
    
    # Keywords commonly found in OTP or verification messages
    keywords = ["otp","One Time Password", "OTP"]
    
    # Check if any keyword exists in the message content
    return any(keyword in content for keyword in keywords)


def process_webhook(source: str, phone: str, data: Dict[str, Any]) -> Optional[str]:
    """
    Process an incoming webhook message and determine if it should be stored.
    
    This function serves as the main processing pipeline for webhook messages.
    It validates input data, checks for OTP content, and decides whether the
    message should be saved to the persistence layer.
    
    Args:
        source (str): The source of the webhook (e.g., 'gupshup', 'twilio')
        phone (str): The phone number associated with the webhook message
        data (Dict[str, Any]): The webhook message data to process
        
    Returns:
        Optional[str]: The message timestamp if it should be persisted, None otherwise
        
    Examples:
        >>> process_webhook("gupshup", "1234567890", {"content": "Your OTP is 123456", "timestamp": "2023-04-22T10:00:00Z"})
        "2023-04-22T10:00:00Z"
        >>> process_webhook("gupshup", "1234567890", {"content": "Hello, how are you?", "timestamp": "2023-04-22T10:00:00Z"})
        None
    """
    # Ensure required fields are present
    if not data or not isinstance(data, dict):
        return None
        
    # Check for OTP keywords - only store messages with OTP content
    if not contains_otp_keywords(data):
        return None
        
    # At this point, message contains OTP and should be persisted
    return data.get("timestamp")
