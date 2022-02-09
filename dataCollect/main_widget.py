# -*- coding: utf-8 -*-
import sys
import os
if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import platform
import ctypes
from ctypes import *
import math
import time
import numpy as np
import cv2

# ui配置文件
cUi, cBase = uic.loadUiType("main_widget.ui")

# 主界面
class CMainWidget(QWidget, cUi):
    def __init__(self):
        # 设置UI
        QMainWindow.__init__(self)
        cUi.__init__(self)
        self.setupUi(self)

        self.save_dir = ''
        self.cap = None
        self.timer = QTimer()
        self.btn_choose_dir.clicked.connect(self.slot_btn_choose_dir)
        self.btn_start.clicked.connect(self.slot_btn_start)

    def slot_btn_choose_dir(self):
        self.save_dir = QFileDialog.getExistingDirectory(self, "choose save dir", "save")
        self.edit_save_dir.setText(self.save_dir)

    def slot_btn_start(self):
        if self.cap is None:
            self.cap = cv2.VideoCapture(int(self.edit_camera.text()), cv2.CAP_DSHOW)
            self.save_dir = self.edit_save_dir.text()
            self.frame = 0
            self.interval = int(self.edit_frame.text())
            self.timer.start()
            self.timer.setInterval(33) #30frames/sec
            self.timer.timeout.connect(self.slot_camera)
            self.btn_start.setText('camera off')
        else:
            self.cap.release()
            self.cap = None
            self.timer.stop()
            self.btn_start.setText('camera on')

    def slot_camera(self):
        if (self.cap.isOpened()):
            # get a frame
            self.frame += 1
            ret, img = self.cap.read()
            height, width, bytesPerComponent = img.shape
            bytesPerLine = bytesPerComponent * width
            img_rgb=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
            self.interval = int(self.edit_frame.text())
            if self.frame % self.interval == 0 and self.checkBox.isChecked():
                label = self.edit_label.text()
                label_dir = self.save_dir + '/' + label
                now_time = int(time.time() * 1000)
                img_path = label_dir + '/%d.jpg'%now_time
                if not os.path.exists(label_dir):
                    os.makedirs(label_dir)
                cv2.imwrite(img_path, img)
                cv2.putText(img_rgb, '%s'%(img_path), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 2)

            self.image = QImage(img_rgb.data, width, height, bytesPerLine, QImage.Format_RGB888)
            self.label_frame.setPixmap(QPixmap.fromImage(self.image).scaled(self.label_frame.width(), self.label_frame.height()))

if __name__ == "__main__":
    cApp = QApplication(sys.argv)
    cMainWidget = CMainWidget()
    cMainWidget.show()
    sys.exit(cApp.exec_())