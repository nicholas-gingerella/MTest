#!/bin/python3

import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.Qt import QPushButton, QCoreApplication

class MainGui(QWidget):
  def __init__(self):
    super().__init__()
    self.initUI()
  
  def initUI(self):
        
        # Set basic geometry and title for window
        self.setGeometry(300, 300, 300, 220)
        self.setWindowTitle('Icon')
        self.setWindowIcon(QIcon('Files/GUI/Icons/test.png'))
        
        # Make a quit button
        quitButton = QPushButton('QUIT', self)
        quitButton.setToolTip('Push this button to quit')
        quitButton.clicked.connect(QCoreApplication.instance().quit)
        quitButton.resize(quitButton.sizeHint())
        quitButton.move(50,50)
    
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = MainGui()
    sys.exit(app.exec_())