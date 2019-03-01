import time
import numpy
import pyaudio
import fluidsynth

pa = pyaudio.PyAudio()
strm = pa.open(
    format = pyaudio.paInt16,
    channels = 2, 
    rate = 44100, 
    output = True)

s = []

fl = fluidsynth.Synth()

# Initial silence is 1 second
s = numpy.append(s, fl.get_samples(44100 * 1))

sfid = fl.sfload("/usr/share/sounds/sf2/FluidR3_GM.sf2")
fl.program_select(0, sfid, 0, 100)

fl.noteon(0, 76, 100)
fl.noteon(0, 83, 100)
fl.noteon(0, 94, 100)

# Chord is held for 2 seconds
s = numpy.append(s, fl.get_samples(44100 * 1))

fl.noteoff(0, 76)
fl.noteoff(0, 83)
fl.noteoff(0, 94)

# Decay of chord is held for 1 second
s = numpy.append(s, fl.get_samples(44100 * 1))

fl.delete()

samps = fluidsynth.raw_audio_string(s*2)

print (len(samps))
print ('Starting playback')
strm.write(samps)
