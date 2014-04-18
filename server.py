import BaseHTTPServer
from cStringIO import StringIO
import urlparse
import pixelBasedMusic

class Handler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write("The server is up. Use a post request with any data to get an mp3 back.")

    def do_POST(self):
        # Extract the contents of the POST
        length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(length)

        with open('tmp.jpg' ,'wb') as image_file:
            image_file.write(post_data)

        composition = pixelBasedMusic.image2midi('./tmp.jpg')
        MidiFileOut.write_Composition('tmp.mid', midi_composition)

        subprocess.call("timidity -Ow ./tmp.mid", shell=True)
        subprocess.call("lame tmp.wav tmp.mp3", shell=True)

        with open('tmp.mp3', 'rb') as song_file:
            self.send_response(200)
            self.send_header("Content-type", "audio/mpeg")
            self.end_headers()
            self.wfile.write(song_file.read())

        subprocess.call("rm tmp.jpg tmp.mid tmp.mp3", shell=True)

PORT = 80

httpd = BaseHTTPServer.HTTPServer(('', PORT), Handler)
print("Servering!")
httpd.serve_forever()
