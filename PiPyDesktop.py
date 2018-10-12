import sys
from PyQt4 import QtGui
from PyQt4 import QtCore
from Clock import Clock
from Weather import Weather

class PiPyDesktop(QtGui.QWidget):

    def __init__(self):
        super(PiPyDesktop, self).__init__()
        grid = QtGui.QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(Clock(), 1, 0)
        grid.addWidget(Weather(), 1, 1)
        self.setLayout(grid)
        self.setWindowTitle('PiPyDesktop')
        self.setStyleSheet("background-color:black;")
        self.setCursor(QtCore.Qt.BlankCursor)
        
def main():

    app = QtGui.QApplication(sys.argv)
    desktop = PiPyDesktop()
    
#    desktop.show()
#    desktop.resize(640, 480)
    desktop.showFullScreen()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()        
