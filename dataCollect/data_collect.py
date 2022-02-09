# -*- coding: utf-8 -*-
import sys
import os
from PyQt5.QtWidgets import *
from main_widget import *

if __name__ == "__main__":
    cApp = QApplication(sys.argv)
    cMainWidget = CMainWidget()
    cMainWidget.show()
    sys.exit(cApp.exec_())