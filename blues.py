from mingus.core import *
from mingus.containers import *
from mingus.midi import MidiFileOut
import mingus.core.scales as scales
from mingus.containers.Note import Note
from mingus.containers.Composition import Composition
import random
import mingus.core.notes as notes


def standard_progression():
    return ['I', 'I', 'I', 'I', 'IV', 'IV', 'I', 'I', 'V', 'V', 'I', 'I']

def shuffle_progression():
    return ['I', 'I', 'I', 'I', 'IV', 'IV', 'I', 'I', 'V', 'IV', 'I', 'I']

def quick_to_four_progression():
    return ['I', 'IV', 'I', 'I', 'IV', 'IV', 'I', 'I', 'V', 'IV', 'I', 'I']

#TODO turnarounds on the last bar (dominant chord or  augmented dominant)

def make_rhythm_bar(chord, key='C'):
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

def rhythm_track(key, progression_type='standard', repititions=1):
    track = Track()

    progression_type = random.choice(['standard','shuffle','quick to four'])
    print("Progression Type: {}".format(progression_type))

    if progression_type is 'standard':
        progression = standard_progression()
    elif progression_type is 'shuffle':
        progression = shuffle_progression()
    elif progression_type is 'quick to four':
        progression = quick_to_four_progression()
    else:
        raise ValueError('invalid progression type')

    for chord in progression*repititions:
       track.add_bar(make_rhythm_bar(chord, key))

    return track

def make_melody_bar(key='C'):
    """Make a bar of melody in the specified key."""
    bar = Bar()
    scale = blues_scale(key)

    note = random.choice(scale)
    note_number = scale.index(note)
    #TODO walk the scale!
    bar.place_notes(note, 4)

    while bar.space_left():
        next_item = random.choice(['quarter note', 'eighth note',
                                   'quarter rest', 'eighth rest'])

        note_number += random.choice([-1,0,1])
        if note_number<0 or note_number>len(scale)-1:
            note = random.choice(scale)
            note_number = scale.index(note)

        if next_item is 'quarter rest':
            pass
            #bar.place_rest(4)
        elif next_item is 'eighth rest':
            bar.place_rest(8)
        elif next_item is 'quarter note':
            bar.place_notes(scale[note_number], 4)
        elif next_item is 'eighth note':
            bar.place_notes(scale[note_number], 8)

    return bar

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
    key = 'C'

    rhythm_track = Track()
    melody_track = Track()

    progression = standard_progression()

    for chord in progression:
        rhythm_track.add_bar(make_rhythm_bar(chord, key))
        melody_track.add_bar(make_melody_bar(key))

    composition = Composition()
    composition.add_track(melody_track)
    composition.add_track(rhythm_track)

    MidiFileOut.write_Composition('blues.mid', composition)

