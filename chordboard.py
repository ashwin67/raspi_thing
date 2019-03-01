import math
import os
import sys
import time
import fluidsynth

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import pyaudio
import numpy as np

class TouchWindow(QWidget):
    def __init__(self, parent=None):
        super(TouchWindow, self).__init__(parent)
        self.text = ""

        # Resizing the sample window to full desktop size:
        frame_rect = app.desktop().frameGeometry()
        self.max_width, self.max_height = frame_rect.width(), frame_rect.height()
        self.resize(self.max_width, self.max_height)
        #self.move(-9, 0)
        self.setWindowTitle("Wacom Draw Area")
        self.width = self.max_width
        self.height = self.max_height
        
        self.audio = pyaudio.PyAudio()
        self.strm = self.audio.open(format = pyaudio.paInt16, channels = 2, rate = 44100, output = True)
        self.fl = fluidsynth.Synth()
        self.sfid = self.fl.sfload("/usr/share/sounds/sf2/FluidR3_GM.sf2")
        self.fl.program_select(0, self.sfid, 0, 100)
        
        self.volume = 50
        self.freq = 50
        self.old_volume = self.volume
        self.old_freq = self.freq

        self.sample_rate = 44100
        self.samples = []
        self.dur = 0.25

    def display(self, mode):
        self.text = 'mode: ' + mode + '\n'
        self.text += 'x: ' + str(self.curr_x) + '\n'
        self.text += 'y: ' + str(self.curr_y)
        self.text += 'Freq: ' + str(self.freq)
        self.text += 'Volume: ' + str(self.volume)
        if mode == 'tablet':
            self.text += '\nPressure: ' + str(self.pen_pressure)

    def emit_sound(self):
        self.freq = int(self.curr_x/40)+65
        self.volume = int((1000-self.curr_y)/9)
        if abs(self.freq - self.old_freq) > 2:
            self.fl.noteon(0, self.freq, self.volume)
            self.fl.noteoff(0, self.old_freq)
            self.old_freq = self.freq
            self.old_volume = self.volume
        else:
            pass
        self.samples = []
        self.samples = np.append(self.samples, self.fl.get_samples(int(self.sample_rate * self.dur)))
        
        #self.fl.noteoff(0, self.freq)
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
