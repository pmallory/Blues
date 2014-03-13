from mingus.core import *
from mingus.containers import *
from mingus.midi import MidiFileOut
import mingus.core.scales as scales
from mingus.containers.Note import Note

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

def make_melody(key, seed):
    """Make a bar of melody in key based on key, a sequence of colors."""
    bar = Bar()
    bar.set_meter((14,4))
    scale = blues_scale(key)

    for note in scale:
        bar.place_notes(note, 4)

    for note in reversed(scale):
        print(note)
        bar.place_notes(note, 4)

    MidiFileOut.write_Bar('scale.mid', bar)

def blues_scale(key):
    """Return a blues scale in a given key"""
    major_scale = list(scales.ionian(key))

    #Use mingus.containers.Note to represent notes so we have octave info
    for i, note in enumerate(major_scale):
        major_scale[i] = Note(note)
        if i>0 and major_scale[i]<major_scale[i-1]:
            major_scale[i].octave_up()

    # mingus.Scales is dumb, this is a workaround =/
    fifth = Note(major_scale[4])
    major_scale[2].diminish()
    major_scale[4].diminish()
    major_scale[6].diminish()
    seventh = Note(major_scale[0])
    seventh.octave_up()

    #assemble the blues scale
    blues_scale = [major_scale[0],
                   major_scale[2],
                   major_scale[3],
                   major_scale[4],
                   fifth,
                   major_scale[6],
                   seventh]

    return blues_scale

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


