import sys
from PIL import Image
from midiutil.MidiFile import MIDIFile
from math import sqrt
import itertools
import numpy as np

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

def rgb2yuv(rgb):
    """
    Convert from the rgb colorspace to yuv. The function takes a rgb triple,
    returns a yuv triple.

    The euclidean distance between two points in yuv colorspace cooresponds
    to their perceived difference much better than rgb distance does.

    http://en.wikipedia.org/wiki/YUV
    """
    rgb_vector = np.array(rgb)
    transformation_matrix = np.array([[0.299, 0.587, 0.114],
                                      [-0.14713, -0.28886, 0.436],
                                      [0.615, -0.51499, -0.10001]])

    yuv_vector = np.dot(transformation_matrix, rgb_vector)

    return tuple(yuv_vector)

if __name__ == "__main__":
    im = Image.open(sys.argv[1])
    pixels = im.load()
    dimensions = im.size

    midiFile = MIDIFile(1)
    midiFile.addTrackName(0, 0, "Piano")
    midiFile.addTempo(0, 0, 120)

    time = 0

    for x, y in itertools.islice(spiral(*dimensions), 100):
        print("RGB: {} Nearest match: {}".format(pixels[x,y], closest_color(pixels[x,y])))
        midiFile.addNote(0, 0, color2note(closest_color(pixels[x,y])), time, 1, 100)
        time += 1

    with open('song.mid', 'wb') as file:
        midiFile.writeFile(file)



