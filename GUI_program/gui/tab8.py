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

        self.evklid = widj_tab1.lile_label_name("evklid", "[Все технологические]\Теплоснабжение\ГП0060 Котельная")
        self.klid = widj_tab1.lile_label_name("klid", "[ВСЕ]\Теплоснабжение\ГП0060 Котельная")

        button_generat = widj_tab1.button_setting("Сгенерировать", self.gerait)

        self.table2 = widj_tab1.table_setting(
            ["Register", "Name"])

        self.table2.setRowCount(1)
        self.table2.setSelectionBehavior(QAbstractItemView.SelectItems)  # Выделяет всю строку

        self.text_panel_view = QTextEdit(objectName="text2")
        self.text_panel_view.setToolTip('Промежуточное значение')

        self.text_pattern = QTextEdit(objectName="text1")
        self.text_pattern.setToolTip('Правила вставки')
        self.text_pattern.setText("""f'''{MARKA}.In := ЭGP0060_BKU_REG_3x{Registrer}.ЗначениеУ;
{MARKA}.Invalid := FC_StatusAI(ANY_TO_DINT(Э{Registrer}.ЗначениеУ_q));'''""")

        main_layout.addWidget(self.text_pattern, 17, 0, 10, 2)

        main_layout.addWidget(self.table2, 0, 0, 17, 1)
        main_layout.addWidget(self.text_panel_view, 0, 1, 17, 1)

        main_layout.addWidget(self.evklid, 17, 2, 1, 2)
        main_layout.addWidget(self.klid, 16, 2, 1, 2)
        main_layout.addWidget(button_generat, 25, 2, 1, 2)
        main_layout.addWidget(widj_tab1.line_btn_simple(self), 0, 2, 1, 2)
        main_layout.addWidget(widj_tab1.button_setting("Очистить", self.table_clean), 17, 2, 1, 2)
        # self.hide_all()

        self.setLayout(main_layout)
        # connet the scroll bar signle to our slot

    def table_clean(self):
        self.table2.setRowCount(1)

    def gerait(self):
        try:
            self.cur = self.con.cursor()
            evaklid, klid = self.get_klids(evaklid=self.evklid.line_edit.text(), klid=self.klid.line_edit.text())
            mass_text = []
            indexes = self.table2.rowCount()
            for row in range(indexes):
                Name = self.table2.item(row, 1).text()
                MARKA = self.get_marka_by_name(Name, klid, evaklid)
                Registrer = self.table2.item(row, 0).text()
                mass_text.append(eval(self.text_pattern.toPlainText()))

            # f'''{MARKA}.In := BITGET(ANY_TO_DINT(ЭGP0060_BKU_REG_3x{Registrer.split('.')[0]}.ЗначениеУ), {Registrer.split('.')[1]});
            # {MARKA}.Invalid := FC_StatusAI(ANY_TO_DINT(ЭGP0060_BKU_REG_3x{Registrer.split('.')[0]}.ЗначениеУ_q));'''

            self.text_panel_view.setText('\n'.join(mass_text))
        except:
            self.text_panel_view.setText("Упс, ошибочка вышла :(")
            return

    def get_marka_by_name(self, name, klid, evaklid):
        select = f"select marka from CARDS where name = '{name}' and  klid= {klid} and evklid = {evaklid}"
        self.cur.execute(select)
        try:
            return [id[0] for id in self.cur][0]
        except:
            return 'None'

    def get_klids(self, evaklid, klid):
        evaid = self.get_id(evaklid, "EVKLASSIFIKATOR")
        kid = self.get_id(klid, "KLASSIFIKATOR")
        return evaid, kid

    def get_id(self, path, table):
        level_of_page = path.split('\\')
        current_parent = None

        for level in level_of_page:
            if current_parent is None:
                select = f"select ID from {table} where name = '{level}'"
            else:
                select = f"select ID from {table} where name = '{level}' and PID = {current_parent}"
            self.cur.execute(select)
            current_parent = [id[0] for id in self.cur][0]

        return current_parent
