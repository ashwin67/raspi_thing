# raspi_thing

Task 1: Get a window working on the raspberry pi where touch and mouse data from the tablet are obtained
* On a raspberry pi (3+), sudo apt-get install qt5-default pyqt5-dev pyqt5-dev-tools
* Dependencies such as sip should automatically be installed.
* pip3 install pyqt5
* I am using a wacom intuos for this task
* python3 tablet.py # Python3 is required

Task 2: Create sound changes based on the touch / mouse data
* sudo apt-get install portaudio19-dev
* sudo apt-get install libatlas-base-dev
* pip3 install pyaudio
* pip3 install numpy
* python3 soundboard.py

Task 3: Create Chords etc using Fluidsynth
* sudo apt-get install fluidsynth
* Download https://github.com/nwhitehead/pyfluidsynth
* sudo python3 setup.py install
* python3 chord.py

Task 4: Change some code and run to get chord sounds from the wacom
* python chordboard.py
