import sys
from PIL import Image
from midiutil.MidiFile import MIDIFile
from math import sqrt
import itertools
import numpy as np
from collections import deque
from scipy.cluster.vq import kmeans

def closest_color(rgb):
# Map color names to their YCbCr values
    colors = {"red": rgb2YCbCr((255, 0, 0)),
              "orange": rgb2YCbCr((255, 165, 0)),
              "yellow": rgb2YCbCr((255, 255, 0)),
              "green": rgb2YCbCr((0, 255, 0)),
              "aqua": rgb2YCbCr((127, 255, 212)),
              "blue": rgb2YCbCr((0, 0, 255)),
              "violet": rgb2YCbCr((143, 0, 255)),
             }

    reference_color = rgb2YCbCr(rgb)

    distances = []
    for color in colors:
        distances.append((euclidean_distance(reference_color,
                          colors[color]), color))


    return min(distances)[1]

def euclidean_distance(p, q):
    return sqrt(sum([(pair[0]-pair[1])**2 for pair in zip(p, q)]))

def color2note(color):
    """ Map color names to notes. """
    notes = {"red": 60,     #middle C
             "orange": 62,  #D
             "yellow": 64,  #E
             "green": 65,   #F
             "aqua": 67,    #G
             "blue": 69,    #A
             "violet": 71,  #B
            }

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
    transformation_matrix = np.array([[ 0.299,  0.587,  0.114],
                                      [-0.169, -0.331,  0.500],
                                      [ 0.500, -0.419, -0.081]])

    YCbCr_vector = scaling_vector + np.dot(transformation_matrix, rgb_vector)

    return tuple(YCbCr_vector)

def YCbCr2rgb(YCbCr):
    """
    Convert from a YCbCr triple to an RGB triple (of ints).

    NOTE: Converting back and forth isn't perfectly precise. The error is less
          than one though and since RGB triples are integers it's okay!
    """
    YCbCr_vector = np.array(YCbCr) + np.array([0, -128, -128])
    transformation_matrix = np.array([[1.0,  0.000,  1.400],
                                      [1.0, -0.343, -0.711],
                                      [1.0,  1.765,  0.000]])

    rgb_vector = np.dot(transformation_matrix, YCbCr_vector)

    return rgb_vector.astype(int)

def dominant_colors(image, k=3):
    """
    Return the k (default 3) dominant colors of an image

    image of of type PIL.Image
    """

    # shrink image so this doesn't take all day
    small_image = image.resize((100, 100))

    # make a numpy array with an RGB triple for each of
    # the 10000 pixels in small_image.
    rgb_matrix = np.array(small_image).reshape(1e4, k)

    # convert values to YCbCr
    YCbCr_matrix = np.apply_along_axis(rgb2YCbCr, 1, rgb_matrix)

    # get the dominant colors with k-means clustering
    YCbCr_dominant_colors = kmeans(YCbCr_matrix, 3)[0]

    #convert back to RGB
    RGB_dominant_colors = np.apply_along_axis(YCbCr2rgb, 1,
                                              YCbCr_dominant_colors)

    return RGB_dominant_colors

def is_monotonous(note, previous_notes):
    """ return True if each of the previous notes is the same as note. """
    return all(note == n for n in previous_notes)

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

    for r, c in itertools.islice(spiral(*dimensions), 100):
        note = color2note(closest_color(pixels[r, c]))

        recent_notes.append(note)

        if not is_monotonous(note, recent_notes):
            midiFile.addNote(0, 0, note, time, 1, 100)
            time += 1

    with open('song.mid', 'wb') as f:
        midiFile.writeFile(f)

