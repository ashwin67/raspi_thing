import math
import os
import sys
import time

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import schedule

class TouchWindow(QWidget):
    def __init__(self, parent=None):
        super(TouchWindow, self).__init__(parent)
        self.text = ""

        # Resizing the sample window to full desktop size:
        frame_rect = app.desktop().frameGeometry()
        width, height = frame_rect.width(), frame_rect.height()
        self.resize(width, height)
        #self.move(-9, 0)
        self.setWindowTitle("Wacom Draw Area")
        self.width = width
        self.height = height

    def display(self, mode):
        self.text = 'mode: ' + mode + '\n'
        self.text += 'x: ' + str(self.curr_x) + '\n'
        self.text += 'y: ' + str(self.curr_y)
        if mode == 'tablet':
            self.text += '\nPressure: ' + str(self.pen_pressure)

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
            
        self.display('tablet')
        tabletEvent.accept()
        self.update()

    def mouseMoveEvent(self, mouseMoveEvent):
        self.curr_x = mouseMoveEvent.globalX()
        self.curr_y = mouseMoveEvent.globalY()
        self.on_mouseMove(mouseMoveEvent)

        self.display('mouse')
        mouseMoveEvent.accept()
        self.update()

    def mousePressEvent(self, mousePressEvent):
        self.curr_x = mousePressEvent.globalX()
        self.curr_y = mousePressEvent.globalY()
        self.on_mousePress(mousePressEvent)

        self.display('mouse')
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
