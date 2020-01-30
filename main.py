# -*- coding:utf-8 -*-
import sys
if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication,QMainWindow
from image_merge_ui import Ui_Form
from image_merge import MainWindow


if __name__ == "__main__":  
	    app = QtWidgets.QApplication(sys.argv) 
	    MainWindow  = MainWindow()
	    MainWindow.show()
	    sys.exit(app.exec_())
