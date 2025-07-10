#!/usr/bin/env python3
"""
Health check endpoint for Railway monitoring
Optional web server for Railway to monitor bot health
"""

import os
import threading
import time
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            health_data = {
                "status": "healthy",
                "timestamp": datetime.now().isoformat(),
                "service": "TRUE ORB Trading Bot",
                "version": "1.0.0"
            }
            
            self.wfile.write(str(health_data).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        # Suppress default logging
        pass

def start_health_server():
    """Start health check server in background thread"""
    port = int(os.getenv('PORT', '8080'))
    
    try:
        server = HTTPServer(('0.0.0.0', port), HealthHandler)
        print(f"🏥 Health check server running on port {port}")
        server.serve_forever()
    except Exception as e:
        print(f"⚠️  Health server failed: {e}")

def run_health_check_background():
    """Run health check server in background thread"""
    health_thread = threading.Thread(target=start_health_server, daemon=True)
    health_thread.start()
    return health_thread

if __name__ == "__main__":
    start_health_server()