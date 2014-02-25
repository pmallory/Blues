import sys
from PIL import Image
from midiutil.MidiFile import MIDIFile
from math import sqrt
import itertools

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

def spiral(N, M):
    """
    Generate the coordinates of pixels along spiraling out from the center.

    Usage:
    for a,b in spiral(5,3):
        print (a,b)

    http://stackoverflow.com/questions/398299/looping-in-a-spiral
    """
    x, y = 0, 0
    dx, dy = 0, -1

    for n in xrange(N*M):
        if abs(x) == abs(y) and [dx,dy] != [1,0] or x>0 and y==1-x:
            dx, dy = -dy, dx    # corner, change direction

        if abs(x)>N/2 or abs(y)>M/2:    #non-square
            dx, dy = -dy, dx    #change directon
            x, y = -y+dx, x+dy  #jump

        yield x+N/2, y+M/2
        x, y = x+dx, y+dy

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



