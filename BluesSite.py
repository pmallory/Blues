from flask import Flask
app = Flask(__name__, static_url_path='')

import blues
from mingus.containers.Composition import Composition
from mingus.containers import *
from mingus.midi import MidiFileOut

@app.route("/")
def hello():
    key = 'G'
    rhythm_track = blues.rhythm_track(key, repititions=1)
    melody_track = Track()
    for bar_number in xrange(12):
        melody_track.add_bar(blues.make_melody_bar(key))

    composition = Composition()
    composition.add_track(melody_track)
    composition.add_track(rhythm_track)

    MidiFileOut.write_Composition('static/Blues.mid', composition)
    return app.send_static_file('Blues.mid')

if __name__ == "__main__":
    app.run()
