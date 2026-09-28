"""
Main Application Module

This is the entry point for the Gupshup Webhook API application.
It creates a Flask application, registers all the necessary blueprints,
adds a health check endpoint, and runs the server if executed directly.

The application handles:
1. Receiving webhook data from external services (e.g., Gupshup)
2. Filtering messages to only store those containing OTP information
3. Providing REST API endpoints to retrieve and manage stored messages

The application architecture follows a modular blueprint-based design,
separating concerns between webhook handling, API endpoints, and data persistence.
"""

from flask import Flask, jsonify

from src.config import Config
from src.api import api_bp
from src.webhook.routes import webhook_bp

def create_app():
    """
    Create and configure the Flask application.
    
    This factory function creates a new Flask application instance,
    registers all blueprints, and adds a health check endpoint.
    Using a factory function allows for easier testing and configuration.
    
    Returns:
        Flask: A configured Flask application instance ready to run
    """
    # Create the Flask application instance
    app = Flask(__name__)
    
    # Register blueprints
    app.register_blueprint(api_bp)
    app.register_blueprint(webhook_bp)
    
    # Add health check endpoint
    @app.route('/health')
    def health_check():
        """
        Health check endpoint to verify the application is running.
        
        This endpoint is useful for:
        - Docker health checks
        - Load balancer checks
        - Monitoring systems
        
        Returns:
            dict: A JSON response with status and environment information
            
        Example response:
            {"status": "ok", "environment": "dev"}
        """
        return jsonify({"status": "ok", "environment": Config.ENV})
    
    return app

# Create the Flask application
app = create_app()

if __name__ == '__main__':
    """
    Run the application directly if this file is executed as a script.
    
    This block is only executed when the file is run directly,
    not when it's imported as a module. It starts the Flask
    development server with the configured host, port, and debug settings.
    
    For production, use a WSGI server like Gunicorn instead.
    """
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)

# Note: In a production environment, consider using a WSGI server like Gunicorn
# or uWSGI to serve the application. The Flask development server is not suitable
# for production use due to performance and security reasons.
# For example, to run with Gunicorn:
# gunicorn -w 4 -b

# Run with env specific settings
# Running with QA configuration
# ENV_NAME=qa python src/app.py