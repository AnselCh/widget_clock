from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from time import strftime
import sys
import threading


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Ann Clock')
        self.setWindowFlags(Qt.WindowStaysOnTopHint)  # 視窗置頂
        self.setWindowFlag(Qt.FramelessWindowHint)  # 標題列消失
        self.setAttribute(Qt.WA_TranslucentBackground)  # 整個label以外設為半透明
        self.resize(360, 110)
        self.setUpdatesEnabled(True)  # 時間更新的Thread
        self.ui()
        self.clock_window = True

    def ui(self):

        self.label_time = QLabel(self)
        font = QFont()
        font.setFamily('calibri')
        font.setPointSize(40)
        font.setBold(True)
        self.label = QLabel(self)
        self.label.setGeometry(140, 90, 100, 30)
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
        self.slider = QSlider(self)
        self.slider.setGeometry(30, 75, 300, 30)
        self.slider.setRange(1, 10)
        self.slider.setValue(5)
        self.slider.setOrientation(1)
        self.slider.setStyleSheet('''
        QSlider {   border-radius: 10px;    }
        QSlider::groove:horizontal {
            height: 5px;
            background: #C2C287;
        }
        QSlider::handle:horizontal{
            background: #FFFFAA;
            width: 16px;
            height: 16px;
            margin:-6px 0;
            border-radius:8px;
        }
        QSlider::sub-page:horizontal{
            background:#A5A552;
        }
        ''')

    def nowtime(self):
        while self.clock_window:
            string = strftime('%H:%M:%S %p')
            self.label_time.setText(string)

    def transparency(self):
        while self.clock_window:
            user_setting = ((self.slider.value())/10)
            tran = user_setting
            self.setWindowOpacity(tran)

    def closeEvent(self, event):
        self.clock_window = False

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
    se = threading.Thread(target=window.transparency)
    clock.start()
    se.start()
    window.show()
    sys.exit(app.exec_())
