Generate random 12 bar blues

Usage example:
```python
import blues
from mingus.containers.Composition import Composition
from mingus.containers import *
from mingus.midi import MidiFileOut

key = 'G'
rhythm_track = blues.rhythm_track(key, repititions=1)
melody_track = Track()
for bar_number in xrange(12):
    melody_track.add_bar(blues.make_melody_bar(key)

composition = Composition()
composition.add_track(melody_track)
composition.add_track(rhythm_track)

MidiFileOut.write_Composition('Blues.mid', composition)
```

Requires FluidSynth,
```bash
apt-get install FluidSynth
or
brew install FluidSynth
``
