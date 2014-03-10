from mingus.core import *
from mingus.containers import *
from mingus.midi import MidiFileOut

key = 'G'
progression = ['I', 'I', 'I', 'I', 'IV', 'IV', 'I', 'I', 'V', 'V', 'I', 'I']

def make_rhythm(key, chord):
    bar = Bar()

    if chord is 'I':
        root_note = chords.tonic(key)[0]
    elif chord is 'II':
        root_note = chords.supertonic(key)[0]
    elif chord is 'III':
        root_note = chords.mediant(key)[0]
    elif chord is 'IV':
        root_note = chords.subdominant(key)[0]
    elif chord is 'V':
        root_note = chords.dominant(key)[0]
    elif chord is 'VI':
        root_note = chords.submediant(key)[0]
    else:
        raise ValueError('invalid chord')

    perfect_fifth = chords.from_shorthand(root_note+'5')
    major_sixth_simple = [chords.major_sixth(root_note)[0],
                          chords.major_sixth(root_note)[-1]]

    bar.place_notes(perfect_fifth, 4)
    bar.place_notes(major_sixth_simple, 4)
    bar.place_notes(perfect_fifth, 4)
    bar.place_notes(major_sixth_simple, 4)

    return down_octave(bar)

def down_octave(bar):
    for chord in [beat[2] for beat in bar]:
        for note in chord:
            note.octave_down()

    return bar

if __name__ == '__main__':
    rhythm_track = Track()

    for chord in progression:
        rhythm_track.add_bar(make_rhythm(key, chord))

    MidiFileOut.write_Track('blues.mid', rhythm_track)


