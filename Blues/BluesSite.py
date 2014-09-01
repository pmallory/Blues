from flask import Flask, Response
app = Flask(__name__, static_url_path='')

import blues
from mingus.containers.Composition import Composition
from mingus.containers import *
from mingus.midi import MidiFileOut as mfo
from mingus.midi.MidiTrack import MidiTrack

@app.route("/")
def main():
    key = 'G'
    rhythm_track = blues.rhythm_track(key, repititions=1)
    melody_track = Track()
    for bar_number in xrange(12):
        melody_track.add_bar(blues.make_melody_bar(key))

    composition = Composition()
    composition.add_track(melody_track)
    composition.add_track(rhythm_track)


    #This is a basically MidiFileOut.write_Composition without the write to a file part
    #TODO patch MidiFileOut
    m = mfo.MidiFile()
    t = []
    for x in range(len(composition.tracks)):
        t += [MidiTrack(120)] #120 bpm
    m.tracks = t
    for i in range(len(composition.tracks)):
        m.tracks[i].play_Track(composition.tracks[i])
    return Response(m.get_midi_data(), mimetype='audio/midi')


if __name__ == "__main__":
    app.run(debug=False)
