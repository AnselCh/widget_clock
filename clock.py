from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from time import strftime
import sys
import threading


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowOpacity(0.3)
        self.setWindowTitle('Ann Clock')
        self.setWindowFlags(Qt.WindowStaysOnTopHint)  # 視窗置頂
        self.setWindowFlag(Qt.FramelessWindowHint)  # 標題列消失
        self.setAttribute(Qt.WA_TranslucentBackground)  # 整個label以外設為半透明
        self.resize(360, 85)
        self.setUpdatesEnabled(True)  # 時間更新的Thread
        self.ui()
        self.ocv = True

    def ui(self):
        self.label_time = QLabel(self)
        font = QFont()
        font.setFamily('calibri')
        font.setPointSize(40)
        font.setBold(True)
        self.label_time.setFont(font)
        self.label_time.setAlignment(Qt.AlignCenter)
        radius = 12
        self.label_time.setStyleSheet('''
            color:	black;
            background:rgb(245, 245, 245);
            border-top-left-radius:{0}px;
            border-bottom-left-radius:{0}px;
            border-top-right-radius:{0}px;
            border-bottom-right-radius:{0}px;
            '''.format(radius))

    def nowtime(self):
        while self.ocv:
            string = strftime('%H:%M:%S %p')
            self.label_time.setText(string)

    def closeEvent(self, event):
        self.ocv = False

    def run(self):
        self.thread_a = QThread()
        self.thread_a.run = self.nowtime
        self.thread_a.start()

    def mousePressEvent(self, event):
        self.oldPosition = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPosition)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPosition = event.globalPos()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWidget()
    clock = threading.Thread(target=window.nowtime)
    clock.start()
    window.show()
    sys.exit(app.exec_())
