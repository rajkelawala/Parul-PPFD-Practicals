from http.server import HTTPServer, SimpleHTTPRequestHandler
HOST = "localhost"
PORT = 8000

class StaticServer(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'  # Route root path to index.html
        return super().do_GET()
    
def run_server():
    with HTTPServer((HOST, PORT), StaticServer) as server:
        print(f"Serving on http://{HOST}:{PORT}")
        server.serve_forever()

if __name__ == "__main__":
    run_server()
