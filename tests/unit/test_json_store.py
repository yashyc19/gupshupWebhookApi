import os
import json
import tempfile
import unittest
from datetime import datetime

from src.persistence.json_store import JsonFilePersistence


class TestJsonFilePersistence(unittest.TestCase):
    def setUp(self):
        """Set up test environment"""
        # Use a temporary directory for tests
        self.temp_dir = tempfile.TemporaryDirectory()
        self.persistence = JsonFilePersistence(self.temp_dir.name)
        
        # Test data
        self.source = "gupshup"
        self.phone = "1234567890"
        self.test_message = {
            "content": "Your OTP code is 123456",
            "timestamp": datetime.utcnow().isoformat()
        }
        
    def tearDown(self):
        """Clean up after tests"""
        self.temp_dir.cleanup()
        
    def test_save_message(self):
        """Test saving a message"""
        # Save the message
        message_id = self.persistence.save_message(self.source, self.phone, self.test_message)
        
        # Verify it was saved
        self.assertEqual(message_id, self.test_message["timestamp"])
        
        # Check the file was created
        file_path = self.persistence._get_file_path(self.source, self.phone)
        self.assertTrue(os.path.exists(file_path))
        
        # Verify content
        with open(file_path, 'r') as f:
            data = json.load(f)
            self.assertIn(message_id, data)
            self.assertEqual(data[message_id], self.test_message)
            
    def test_get_messages(self):
        """Test getting all messages"""
        # Save a message first
        message_id = self.persistence.save_message(self.source, self.phone, self.test_message)
        
        # Get all messages
        messages = self.persistence.get_messages(self.source, self.phone)
        
        # Verify we got the message back
        self.assertIn(message_id, messages)
        self.assertEqual(messages[message_id], self.test_message)
        
    def test_get_message(self):
        """Test getting a specific message"""
        # Save a message first
        message_id = self.persistence.save_message(self.source, self.phone, self.test_message)
        
        # Get the message
        message = self.persistence.get_message(self.source, self.phone, message_id)
        
        # Verify we got the message back
        self.assertEqual(message, self.test_message)
        
        # Try getting a non-existent message
        non_existent = self.persistence.get_message(self.source, self.phone, "nonexistent")
        self.assertIsNone(non_existent)
        
    def test_delete_message(self):
        """Test deleting a message"""
        # Save a message first
        message_id = self.persistence.save_message(self.source, self.phone, self.test_message)
        
        # Delete the message
        success = self.persistence.delete_message(self.source, self.phone, message_id)
        
        # Verify deletion was successful
        self.assertTrue(success)
        
        # Verify message is gone
        message = self.persistence.get_message(self.source, self.phone, message_id)
        self.assertIsNone(message)
        
        # Try deleting a non-existent message
        success = self.persistence.delete_message(self.source, self.phone, "nonexistent")
        self.assertFalse(success)


if __name__ == '__main__':
    unittest.main()
