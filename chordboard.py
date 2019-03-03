import math
import os
import sys
import time
import fluidsynth

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

notes = [
54, #b1
55, #c2
57, #d2
59, #e2
60, #f2
62, #g2
64, #a2
66, #b2
67, #c3
69  #d3
]
notes_mapping = [
[0,10],
[11,20],
[21,30],
[31,40],
[41,50],
[51,60],
[61,70],
[71,80],
[81,90],
[91,100]
]
import pyaudio
#import numpy as np

class TouchWindow(QWidget):
    def __init__(self, parent=None):
        # Initialize a QT window
        super(TouchWindow, self).__init__(parent)
        self.text = ""
        # Resizing the sample window to full desktop size:
        frame_rect = app.desktop().frameGeometry()
        self.max_width, self.max_height = frame_rect.width(), frame_rect.height()
        self.resize(self.max_width, self.max_height)
        self.width = self.max_width
        self.height = self.max_height
        self.setWindowTitle("Wacom Draw Area")

        # Create Audio
        self.audio = pyaudio.PyAudio()
        self.sample_rate = 44100
        self.strm = self.audio.open(format = pyaudio.paInt16, channels = 2, rate = self.sample_rate, output = True)
        self.fl = fluidsynth.Synth()
        self.sfid = self.fl.sfload("/usr/share/sounds/sf2/FluidR3_GM.sf2") #TODO: Remove this hard coding later
        self.fl.program_select(0, self.sfid, 0, 2)

        # Initialize some values
        self.volume = 50
        self.n1 = 50
        self.old_volume = self.volume
        self.old_n1 = self.n1
        self.samples = []
        self.dur = 0.25

    def display(self, mode):
        self.text = 'mode: ' + mode + '\n'
        self.text += 'x: ' + str(self.curr_x) + '\n'
        self.text += 'y: ' + str(self.curr_y)
        self.text += 'Freq: ' + str(self.n1)
        self.text += 'Volume: ' + str(self.volume)
        if mode == 'tablet':
            self.text += '\nPressure: ' + str(self.pen_pressure)

    def emit_sound(self):
        x_rel = int(100*self.curr_x/self.width)
        self.volume = 0
        for i in range(len(notes_mapping)):
            if (x_rel >= notes_mapping[i][0] and x_rel <= notes_mapping[i][1]):
                self.n1 = notes[i]
                self.volume = 100
                break

        if abs(self.n1 - self.old_n1) >= 1:
            self.fl.noteon(0, self.n1, self.volume)
            self.fl.noteoff(0, self.old_n1)
            self.old_n1 = self.n1
            self.old_volume = self.volume
        else:
            pass
        self.samples = self.fl.get_samples(int(self.sample_rate * self.dur))

        #self.fl.noteoff(0, self.n1)
        #self.samples = np.append(self.samples, self.fl.get_samples(int(self.sample_rate * self.dur)))

        samps = fluidsynth.raw_audio_string(self.samples)
        self.strm.write(samps)

    def on_tabletPress(self, tabletEvent):
        print ('Pen Down at:', self.curr_x, self.curr_y)

    def on_tabletMove(self, tabletEvent):
        print ('Pen:', self.curr_x, self.curr_y, self.pen_pressure)

    def on_tabletRelease(self, tabletEvent):
        print ('Pen Up at:', self.curr_x, self.curr_y)

    def on_mousePress(self, mousePressEvent):
        print ('Mouse Down at:', self.curr_x, self.curr_y)

    def on_mouseMove(self, mouseMoveEvent):
        print ('Mouse:', self.curr_x, self.curr_y)


    def tabletEvent(self, tabletEvent):
        self.curr_x = tabletEvent.globalX()
        self.curr_y = tabletEvent.globalY()
        self.pen_pressure = int(tabletEvent.pressure() * 100)

        if tabletEvent.type() == QTabletEvent.TabletPress:
            self.on_tabletPress(tabletEvent)
        elif tabletEvent.type() == QTabletEvent.TabletMove:
            self.on_tabletMove(tabletEvent)
        elif tabletEvent.type() == QTabletEvent.TabletRelease:
            self.on_tabletRelease(tabletEvent)

        self.emit_sound()
        self.display('tablet')
        tabletEvent.accept()
        self.update()

    def mouseMoveEvent(self, mouseMoveEvent):
        self.curr_x = mouseMoveEvent.globalX()
        self.curr_y = mouseMoveEvent.globalY()
        self.on_mouseMove(mouseMoveEvent)

        self.display('mouse')
        self.emit_sound()
        mouseMoveEvent.accept()
        self.update()

    def mousePressEvent(self, mousePressEvent):
        self.curr_x = mousePressEvent.globalX()
        self.curr_y = mousePressEvent.globalY()
        self.on_mousePress(mousePressEvent)

        self.display('mouse')
        self.emit_sound()
        mousePressEvent.accept()
        self.update()

    def paintEvent(self, event):
        text = self.text
        i = text.find("\n\n")
        if i >= 0:
            text = text.left(i)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.TextAntialiasing)
        painter.drawText(self.rect(), Qt.AlignTop | Qt.AlignLeft , text)

app = QApplication(sys.argv)
mainform = TouchWindow()
mainform.show()
app.exec_()
