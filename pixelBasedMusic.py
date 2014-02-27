import sys
from PIL import Image
from midiutil.MidiFile import MIDIFile
from math import sqrt
import itertools
import numpy as np

def rgb2YCbCr(rgb):
    """
    Convert from the rgb colorspace to YCbCr. The function takes a rgb triple,
    returns a YCbCr triple. The range of values for both RGB and 2YCbCr is
    0 to 255.

    The euclidean distance between two points in YCbCr colorspace corresponds
    to their perceived difference much better than rgb distance does.

    http://en.wikipedia.org/wiki/YUV
    http://www.equasys.de/colorconversion.html
    """
    rgb_vector = np.array(rgb)
    scaling_vector = np.array([0.0, 128.0, 128.0])
    transformation_matrix = np.array([[0.299,  0.587,  0.114],
                                      [-0.169, -0.331, 0.500],
                                      [0.500,  -0.419, -0.081]])

    YCbCr_vector = scaling_vector + np.dot(transformation_matrix, rgb_vector)

    return tuple(YCbCr_vector)

# Map color names to their YCbCr values
colors = {"red": rgb2YCbCr((255 ,0 , 0)),
          "orange": rgb2YCbCr((255, 165, 0)),
          "yellow": rgb2YCbCr((255 ,255 , 0)),
          "green": rgb2YCbCr((0, 255, 0)),
          "aqua": rgb2YCbCr((127, 255, 212)),
          "blue": rgb2YCbCr((0, 0, 255)),
          "violet": rgb2YCbCr((143, 0, 255)),
         }

# Map color names to notes
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
        distances.append((euclidean_distance(rgb2YCbCr(rgb), colors[color]), color))

    return min(distances)[1]

def euclidean_distance(p, q):
    return sqrt(sum(map(lambda pair: (pair[0]-pair[1])**2, zip(p,q))))

def color2note(color):
   return notes.get(color)

def spiral(X, Y):
    """
    Generate the coordinates of pixels along spiraling out from the center.
    This generates coordinates such that (0,0) is the top left corner.

    Usage:
    for a,b in spiral(5,3):
        print (a,b)

    http://stackoverflow.com/questions/398299/looping-in-a-spiral
    """
    x = y = 0
    dx = 0
    dy = -1
    for i in range(max(X, Y)**2):
        if (-X/2 < x <= X/2) and (-Y/2 < y <= Y/2):
            yield x+X/2, y+Y/2
        if x == y or (x < 0 and x == -y) or (x > 0 and x == 1-y):
            dx, dy = -dy, dx
        x, y = x+dx, y+dy

def rgb2YCbCr(rgb):
    """
    Convert from the rgb colorspace to YCbCr. The function takes a rgb triple,
    returns a YCbCr triple. The range of values for both RGB and 2YCbCr is
    0 to 255.

    The euclidean distance between two points in YCbCr colorspace corresponds
    to their perceived difference much better than rgb distance does.

    http://en.wikipedia.org/wiki/YUV
    http://www.equasys.de/colorconversion.html
    """
    rgb_vector = np.array(rgb)
    scaling_vector = np.array([0.0, 128.0, 128.0])
    transformation_matrix = np.array([[0.299,  0.587,  0.114],
                                      [-0.169, -0.331, 0.500],
                                      [0.500,  -0.419, -0.081]])

    YCbCr_vector = scaling_vector + np.dot(transformation_matrix, rgb_vector)

    return tuple(YCbCr_vector)


def isMonotonous(note, previous_notes):
    return note is previous_notes[0] is previous_notes[1] \
                is previous_notes[2] is previous_notes[3]

if __name__ == "__main__":
    im = Image.open(sys.argv[1])
    pixels = im.load()
    dimensions = im.size

    midiFile = MIDIFile(1)
    midiFile.addTrackName(0, 0, "Piano")
    midiFile.addTempo(0, 0, 120)

    time = 0

    # Keep track of recent notes so we don't play the same one
    # five times in a row.
    recent_notes = deque([None]*4, 4)

    for x, y in itertools.islice(spiral(*dimensions), 100):
        note = color2note(closest_color(pixels[x,y]))

        recent_notes.append(note)

        if (not isMonotonous(note, recent_notes)):
            midiFile.addNote(0, 0, note, time, 1, 100)
            time += 1

    with open('song.mid', 'wb') as file:
        midiFile.writeFile(file)

