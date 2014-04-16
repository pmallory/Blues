import BaseHTTPServer
from cStringIO import StringIO

class Handler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write("The server is up. Use a post request with any data to get an mp3 back.")

    def do_POST(self):
        length = int(self.headers.getheader('content-length'))
        data = cgi.parse_qs(self.rfile.read(length), keep_blank_values=1)

        with open('image.jpg', 'w') as img_file:
            img_file.write(data)

        with open('test.mp3', 'rb') as song_file:
            self.send_response(200)
            self.send_header("Content-type", "audio/mpeg")
            self.end_headers()
            self.wfile.write(song_file.read())


PORT = 80

httpd = BaseHTTPServer.HTTPServer(('', PORT), Handler)
print("Servering!")
httpd.serve_forever()
