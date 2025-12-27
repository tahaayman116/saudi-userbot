#!/usr/bin/env python3
"""
Keep alive server for Replit
Runs a simple web server to keep the Repl active
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import logging

logger = logging.getLogger(__name__)

class KeepAliveHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests"""
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Saudi User Bot - Keep Alive</title>
            <meta charset="utf-8">
            <style>
                body {
                    font-family: Arial, sans-serif;
                    text-align: center;
                    padding: 50px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                }
                .container {
                    background: rgba(255,255,255,0.1);
                    padding: 30px;
                    border-radius: 10px;
                    backdrop-filter: blur(10px);
                }
                h1 { margin: 0; font-size: 2.5em; }
                p { font-size: 1.2em; margin-top: 20px; }
                .status { 
                    display: inline-block;
                    width: 15px;
                    height: 15px;
                    background: #4ade80;
                    border-radius: 50%;
                    animation: pulse 2s infinite;
                }
                @keyframes pulse {
                    0%, 100% { opacity: 1; }
                    50% { opacity: 0.5; }
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🤖 Saudi User Bot</h1>
                <p><span class="status"></span> البوت يعمل الآن</p>
                <p>Bot is running and monitoring groups</p>
            </div>
        </body>
        </html>
        """
        
        self.wfile.write(html.encode())
    
    def log_message(self, format, *args):
        """Suppress default logging"""
        pass

def keep_alive():
    """Start keep alive web server"""
    server = HTTPServer(('0.0.0.0', 8080), KeepAliveHandler)
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()
    logger.info("✅ Keep-alive server started on port 8080")

if __name__ == '__main__':
    keep_alive()
    print("Keep-alive server is running...")
    import time
    while True:
        time.sleep(1)
