import sys
from PIL import Image
from midiutil.MidiFile import MIDIFile
from math import sqrt

colors = {"red": (255 ,0 , 0),
          "orange": (255, 165, 0),
          "yellow": (255 ,255 , 0),
          "green": (0, 255, 0),
          "aqua": (127, 255, 212),
          "blue": (0, 0, 255),
          "violet": (143, 0, 255),
         }

notes = {"red": 60,     #middle C
         "orange": 62,  #D
         "yellow": 64,  #E
         "green": 65,   #F
         "aqua": 67,    #G
         "blue": 69,    #A
         "violet": 71,  #B
        }

def closest_color(rgb):
    distances = []
    for color in colors:
        distances.append((euclidean_distance(rgb, colors[color]), color))

    return min(distances)[1]

def euclidean_distance(p, q):
    return sqrt(sum(map(lambda pair: (pair[0]-pair[1])**2, zip(p,q))))

def color2note(color):
   return notes.get(color)

if __name__ == "__main__":
    im = Image.open(sys.argv[1])
    pixels = im.load()
    dimensions = im.size

    midiFile = MIDIFile(1)
    midiFile.addTrackName(0, 0, "Piano")
    midiFile.addTempo(0, 0, 120)

    time = 0

    for i in range(100):
        midiFile.addNote(0, 0, color2note(closest_color(pixels[0,i])), time, 1, 100)
        time += 1

    with open('song.mid', 'wb') as file:
        midiFile.writeFile(file)



