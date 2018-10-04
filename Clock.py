import sys
from PyQt4 import QtGui
from PyQt4 import QtCore
import math
import datetime

class Clock(QtGui.QWidget):
    
    def __init__(self, demoMode = False):
        super(Clock, self).__init__()

        self.setWindowTitle('Clock')
        self.demoMode = demoMode

        self.hour = 0;
        self.minute = 0;
        self.second = 0;
        
        self.ctimer = QtCore.QTimer()
        self.ctimer.timeout.connect(self.tick)
        if (demoMode):
            self.ctimer.start(10)
        else:
            self.ctimer.start(1000) # 1 second
        
        self.hourPen = QtGui.QPen(QtGui.QBrush(QtCore.Qt.white), 8)
        self.minutePen = QtGui.QPen(QtGui.QBrush(QtCore.Qt.lightGray), 3)
        self.secondPen = QtGui.QPen(QtCore.Qt.red)
        
        self.tick()

    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        qp.setRenderHint(QtGui.QPainter.Antialiasing, True)

        # work out the centre
        cx = self.width() / 2
        cy = self.height() / 2
        smallestDimension = min(self.width(),self.height())
        radius = smallestDimension / 2.8
        hourMark = (smallestDimension / 2 - radius) * 0.8

        # draw dial
        qp.setPen(QtCore.Qt.white)
        for hour in range(0,12):
            angle = 2 * math.pi / 12 * hour 
            qp.drawLine(cx + radius * math.sin(angle),
                        cy - radius * math.cos(angle),
                        cx + (radius + hourMark) * math.sin(angle),
                        cy - (radius + hourMark) * math.cos(angle))

        # copy instance variables to local (because we change the value of hour)
        hour = self.hour
        if (hour > 11):
            hour = hour - 12

        # draw the hour hand
        qp.setPen(self.hourPen)
        angle = 2 * math.pi / 12 * (hour + self.minute/60.0)
        qp.drawLine(cx, cy, cx + radius * math.sin(angle), cy - radius * math.cos(angle))

        # draw the minute hand
        qp.setPen(self.minutePen)
        angle = 2 * math.pi / 60 * (self.minute + self.second/60.0) 
        qp.drawLine(cx, cy, cx + radius * 0.8 * math.sin(angle), cy - radius * 0.8 * math.cos(angle))

        # draw the second hand
        qp.setPen(self.secondPen)
        angle = 2 * math.pi / 60 * self.second
        qp.drawLine(cx, cy, cx + radius * 0.8 * math.sin(angle), cy - radius * 0.8 * math.cos(angle))

        # draw the shaft (ooer!)
        qp.setPen(QtGui.QPen(QtCore.Qt.gray))
        qp.setBrush(QtCore.Qt.gray)
        qp.drawEllipse(cx - 8, cy - 8, 16, 16)

        qp.end()


    def tick(self):
        if (self.demoMode):
            self.second = self.second + 1
            if (self.second > 59):
                self.second = 0
                self.minute = self.minute + 1
                if (self.minute > 59):
                    self.minute = 0
                    self.hour = self.hour + 1
                    if (self.hour > 23):
                        self.hour = 0
        else:
            now = datetime.datetime.now()
            self.hour = now.hour
            self.minute = now.minute
            self.second = now.second

        self.update()

    def mousePressEvent(self, event):
        if type(event) == QtGui.QMouseEvent:
            sys.exit()


def main():

    app = QtGui.QApplication(sys.argv)
    w = Clock()
    w.tick() # update clock before showing
    w.show()
    w.setGeometry(300, 300, 250, 150)
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()