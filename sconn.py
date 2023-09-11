import http.server
import socketserver


PORT = 7010 

class SimpleHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Set headers to allow CORS
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', 'http://localhost:3000')
        self.send_header('Access-Control-Allow-Credentials', 'true')
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        self.send_header('Set-Cookie', 'visitor=yes; HttpOnly; SameSite=None; Secure')

        self.wfile.write(b'Cookie set successfully')

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), SimpleHandler) as httpd:
        print(f"Serving at port {PORT}")
        httpd.serve_forever()