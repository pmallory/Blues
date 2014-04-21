import BaseHTTPServer
from cStringIO import StringIO
import urlparse
import pixelBasedMusic
from mingus.midi import MidiFileOut
import subprocess
import datetime
import cgi
import os
import random

class Handler(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "audio/mpeg")
        self.end_headers()
        with open('tmp.mp3', 'rb') as song_file:
            self.send_response(200)
            self.send_header("Content-type", "audio/mpeg")
            self.end_headers()
            self.wfile.write(song_file.read())

    def do_POST(self):
        print self.headers
        length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(length)

        if (os.path.isfile('accumulator.jpg')):
            with open('accumulator.jpg', 'ab') as partial_file:
                partial_file.write(post_data[500:])
        else:
            with open('accumulator.jpg', 'wb') as partial_file:
                partial_file.write(post_data[:141])

        if os.path.getsize("accumulator.jpg") < (length*4*0.9):
            return

        composition = pixelBasedMusic.image2midi('accumulator.jpg')
        tempo = random.randrange(60, 140 , 5)
        MidiFileOut.write_Composition('tmp.mid', composition, tempo)

        print('bpm: {}'.format(tempo))

        subprocess.call("timidity -Ow tmp.mid", shell=True)
        subprocess.call("lame tmp.wav tmp.mp3", shell=True)

        #subprocess.call("rm tmp.wav tmp.jpg tmp.mid", shell=True)

PORT = 80

httpd = BaseHTTPServer.HTTPServer(('', PORT), Handler)
print("Servering!")
httpd.serve_forever()
