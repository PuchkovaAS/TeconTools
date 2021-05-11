# -*- coding: cp1251 -*-
from collections import namedtuple

from PyQt5.QtWidgets import *

import gui.widgets.widj_tab1 as widj_tab1

row_data = namedtuple('row_data', 'kadr evklass main')


class Tab(QWidget):
    def __init__(self):
        super().__init__()
        self.rows = []
        self.initData()
        self.initUI()

    def initData(self):
        self.rows = []
        self.main_title = None

    def initUI(self):

        main_layout = QGridLayout()

        self.table = widj_tab1.table_setting(
            ["Name"])
        self.table.setSelectionBehavior(QAbstractItemView.SelectItems)  # Выделяет всю строку
        self.table.setRowCount(1)

        self.prefix = widj_tab1.lile_label_name("Префикс", "")

        button_generat = widj_tab1.button_setting("Сгенерировать", self.gerait)

        self.table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.table2 = widj_tab1.table_setting(
            ["Name", "Marka"])
        self.table2.setFixedHeight(400)
        self.table2.setRowCount(1)
        self.table3 = widj_tab1.table_setting(
            ["Marka"])
        self.table3.setFixedWidth(800)

        main_layout.addWidget(self.table, 0, 0, 27, 1)
        main_layout.addWidget(self.table3, 0, 1, 27, 1)
        main_layout.addWidget(self.table2, 27, 0, 1, 2)

        main_layout.addWidget(self.prefix, 17, 2, 1, 2)
        main_layout.addWidget(button_generat, 27, 2, 1, 2)

        # self.hide_all()

        self.setLayout(main_layout)
        # connet the scroll bar signle to our slot
        self.table.verticalScrollBar().valueChanged.connect(self.__chnge_position)
        self.table3.verticalScrollBar().valueChanged.connect(self.__chnge_position)

    def __chnge_position(self, index):
        # slot to change the scroll bar  position of all table
        self.table.verticalScrollBar().setValue(index)
        self.table3.verticalScrollBar().setValue(index)

    def gerait(self):
        dict_words = {}

        for idx in range(self.table2.rowCount() - 1):
            dict_words.update({self.table2.item(idx, 0).text(): self.table2.item(idx, 1).text()})

        self.table3.setRowCount(self.table.rowCount())

        for idx in range(self.table.rowCount()):
            row = idx
            col = 0
            word = self.table.item(row, col).text()
            new_word = self.prefix.line_edit.text()
            for key in dict_words.keys():
                if word.find(key) != -1:
                    new_word += '_' + dict_words[key]

            self.table3.setItem(row, col, QTableWidgetItem(new_word))
