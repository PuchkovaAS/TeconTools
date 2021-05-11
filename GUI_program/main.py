from collections import namedtuple
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtGui import QColor
import sys
import os

import gui.tab1_1 as tab1
import gui.tab2 as tab2
import gui.tab4_code as tab4
import gui.tab5_qDock as tab5
import gui.tab10_copy as tab10
import gui.tab11_fbd_copy as tab11
# import gui.tab20 as tab12
# import gui.tab21 as tab14
import gui.tab_xml as tab13
import gui.tab_viewer as tab15
row_data = namedtuple('row_data', 'kadr evklass main')
f = open('LybPyQT5/style/darksource.stylesheet', 'r')
style = f.read()


# Для импорта в Exe pict
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    # base_path = os.path.abspath("/image/")
    return os.path.join(base_path, relative_path)


class Main_Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initGUI()

    def initGUI(self):
        self.setStyleSheet(style)

        self.setWindowIcon(QIcon(resource_path('resources/main_ico.png')))
        self.setMinimumWidth(1500)

        # Цвет
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor('#666666'))
        self.setPalette(palette)

        # Основа
        self.setWindowTitle("Всякое разное")
        self.setMinimumHeight(700)
        self.setMinimumWidth(1000)
        central_widget = QWidget(self)  # Создаём центральный виджет
        self.setCentralWidget(central_widget)  # Устанавливаем центральный виджет

        # Создание вкладок
        self.tab = QTabWidget()
        self.tab.setAutoFillBackground(True)
        self.tab.setPalette(palette)
        self.tab.addTab(tab1.Tab(), "  Меню генератор  ")
        self.tab.addTab(tab2.Tab(), "  Тиражирование  ")
        self.tab.addTab(tab4.Tab(), "  Код  ")
        self.tab.addTab(tab5.Tab(), "  FBD_view FROM ST  ")
        self.tab.addTab(tab10.Tab(), "  Тиражирование граф. эл-тов  ")
        self.tab.addTab(tab11.Tab(), "  Тиражирование FBD эл-тов  ")
        # # self.tab.addTab(tab12.Tab(), "  Копирование св-в каналов  ")
        self.tab.addTab(tab13.Tab(), "  XML <Beautifier/> ")
        # # self.tab.addTab(tab14.Tab(), "  Функция доступа ")
        self.tab.addTab(tab15.Tab(), "  SQL View ")

        main_layout = QHBoxLayout()
        main_layout.addWidget(self.tab)

        central_widget.setLayout(main_layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    root = Main_Window()
    root.showMaximized()
    sys.exit(app.exec_())
