# -*- coding: cp1251 -*-
from xml.dom import minidom

from PyQt5.QtWidgets import *
from bs4 import BeautifulSoup

import gui.widgets.widj_tab1 as widj_tab1
from LybPyQT5.widgets.button import SimpleBtn
from LybPyQT5.widgets.check_box import CheckBox
from LybPyQT5.widgets.tab import LibTab
from LybPyQT5.widgets.text_editor import TextEditor
from PyQt5.QtCore import Qt

class Tab(LibTab):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.text_panel_code = TextEditor(objectName="text3", tooltip='Ugly')

        self.check_box_line = CheckBox(label="Minidom(0)\nBS4(1)")
        # self.check_box_line.cb.stateChanged.connect(self.hideTable)

        button_generat = SimpleBtn(label="Вжух", click_func=self.generat, width=200)

        self.text_panel_view = TextEditor(objectName="text2", tooltip='Beauty')

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.text_panel_code)
        splitter.addWidget(self.text_panel_view)

        self.main_layout.addWidget(splitter, 0, 0, 5, 2)
        self.main_layout.addWidget(self.check_box_line, 1, 2, 1, 1)
        self.main_layout.addWidget(button_generat, 2, 2, 1, 1)

    def generat(self):
        text = self.text_panel_code.toPlainText().replace('', '')
        try:
            if self.check_box_line.isChecked():
                bs = BeautifulSoup(text, 'xml')
                xml_pretty_str = bs.prettify()
            else:
                xml = minidom.parseString(text)
                xml_pretty_str = xml.toprettyxml()
            xml_pretty_str = xml_pretty_str.replace('<?xml version="1.0" ?>', '<?xml version="1.0" encoding="UTF-8"?>')
            self.text_panel_view.setText(xml_pretty_str)
        except Exception as e:
            QMessageBox().warning(self, "Ошибка", str(e), QMessageBox.Ok,
                                  QMessageBox.Ok)
