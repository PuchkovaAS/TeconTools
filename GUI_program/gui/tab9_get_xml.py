# -*- coding: cp1251 -*-
import xml.dom.minidom
from collections import namedtuple

from PyQt5.QtWidgets import *
from jinja2 import BaseLoader
from jinja2 import Environment, FileSystemLoader

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
            ["MARKA", "NAME", "KLASSNAME", "EVKLASSNAME", "PLCNAME", "PLC_ADRESS", "OBJSIGN"])
        self.table.setSelectionBehavior(QAbstractItemView.SelectItems)  # Выделяет всю строку

        button_open = widj_tab1.button_setting("Открыть xml", self.open_xml)
        button_except = widj_tab1.button_setting("Добавить", self.tab_view)
        button_clean = widj_tab1.button_setting("Очистить", self.table_clean)
        button_generat = widj_tab1.button_setting("Сгенерировать", self.gerait_xml)
        self.xml_template = QLabel("None")
        self.xml_template.setWordWrap(True)

        self.text_panel = QTextEdit()
        self.text_panel.setText(
            """[dict(MARKA=f"GP0011_SPPV_{item1}", NAME=f"{item2}", OBJSIGN=f"P", KLASSNAME="[ВСЕ]\Водоснабжение\ГП0011 СППВ", EVKLASSNAME="[Все технологические]\Водоснабжение\ГП0011 СППВ", PLCNAME="ICore_2") for item1, item2 in [["K12_WORK", "Работа"], ["K12_ALARM", "Авария"],["K13_WORK", "Работа"], ["K13_ALARM", "Авария"]]]""")

        self.table.setMaximumWidth(1700)
        self.table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        main_layout.addWidget(self.table, 0, 0, 27, 1)
        # main_layout.addWidget(self.text_panel, 27, 0, 1, 1)
        # main_layout.addWidget(self.xml_template, 12, 2, 1, 2)

        main_layout.addWidget(button_clean, 15, 2, 1, 2)
        # main_layout.addWidget(button_except, 15, 2, 1, 1)
        main_layout.addWidget(button_open, 14, 2, 1, 2)

        # main_layout.addWidget(button_generat, 27, 2, 1, 2)

        # self.hide_all()

        self.setLayout(main_layout)

    def table_clean(self):
        self.table.setRowCount(0)

    def tab_view(self):
        # exec(f'connection = {self.text_panel.toPlainText()}')
        # connection = eval('[dict(MARKA=f"GP0011_SPPV_{item1}_P", NAME=f"{item2}",OBJSIGN=f"P",KLASSNAME="[ВСЕ]\Водоснабжение\ГП0011 СППВ",EVKLASSNAME="[Все технологические]\Водоснабжение\ГП0011 СППВ", PLCNAME="ICore_2") for item1, item2 in [["TO_K1", "Давление на входе насоса K1"],["FROM_K1", "Рабочее давление K1"],["TO_K8", "Давление на входе насоса K8"],["FROM_K8", "Рабочее давление K8"],["TO_K10", "Давление на входе насоса K10"],["FROM_K10", "Рабочее давление K10"],["TO_K14", "Давление на входе насоса K14"],["FROM_K14","Рабочее давление K14"]]]')
        # connection = eval(self.text_panel.toPlainText())
        pass

    def open_xml(self):
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        path, _ = QFileDialog.getOpenFileName(self, 'Открыть xml', "", "Xml (*.xml)", options=options)

        if path == '':
            return

        with open(path, "r", encoding='UTF-8') as f:
            # contents = f.read()#.encode().decode('utf-8')
            dom = xml.dom.minidom.parse(path)
            dom.normalize()
            itemlist = dom.getElementsByTagName('TEHOBJ')
            for item in itemlist:
                # print()
                # print()
                # print()
                #  = "{{NAME}}"
                #  = "{{PLCNAME}}"
                #  = "{{OBJSIGN}}"
                #  = "{{PLC_ADRESS}}"

                index = self.table.rowCount()
                self.table.setRowCount(index + 1)  # и одну строку в таблице
                self.table.setRowHeight(index, 50)

                # self.table.setCellWidget(index, 0, widj_tab1.lineWap(conn.get('MARKA', '')))
                self.table.setItem(index, 0, QTableWidgetItem(item.attributes['MARKA'].value))
                self.table.setItem(index, 1, QTableWidgetItem(item.attributes['NAME'].value))
                self.table.setItem(index, 2, QTableWidgetItem(item.attributes['KLASSNAME'].value))
                self.table.setItem(index, 3, QTableWidgetItem(item.attributes['EVKLASSNAME'].value))
                self.table.setItem(index, 4, QTableWidgetItem(item.attributes['PLCNAME'].value))
                self.table.setItem(index, 5, QTableWidgetItem(item.attributes['PLC_ADRESS'].value))
                self.table.setItem(index, 6, QTableWidgetItem(item.attributes['OBJSIGN'].value))
            self.table.resizeRowsToContents()

            # now = datetime.now()
            # self.xml_template.setText(path + '\n' + str(now.hour) + ':' + str(now.minute) + ':' + str(now.second))
            # # # Сохраняем
            # options = QFileDialog.Options()
            # options |= QFileDialog.DontUseNativeDialog
            # fileName, _ = QFileDialog.getSaveFileName(self, "Сохранить html", "", "html (*.html)", options=options)
            #
            # if fileName == '':
            #     return
            #
            # if fileName.find('.html') == -1:
            #     fileName += '.html'

            # self.template_t = dom.toxml()
            # self.template_t = self.template_t.replace('<?xml version="1.0" ?><root>', '')
            # self.template_t = self.template_t.replace('</root>', '')
            # # dom.writexml(open(fileName, 'w'))
            # with open(fileName, 'w') as file:
            #     file.write(self.template_t)
            #
            # self.table1.setRowCount(1)  # и одну строку в таблице

    def gerait_xml(self):
        template1 = Environment(loader=BaseLoader).from_string(self.template_t)
        env = Environment(loader=FileSystemLoader('.'))
        template = env.get_template('templates/tab2/main_.html')
        contents = []
        # connection = eval(self.text_panel.toPlainText())
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "Сохранить xml", "", "xml (*.xml)", options=options)

        if fileName == '':
            return

        if fileName.find('.xml') == -1:
            fileName += '.xml'

        with open(fileName, "w", encoding='utf8') as f:
            count = self.table.rowCount()
            for index in range(count):
                contents.append(str(
                    template1.render(MARKA=self.check_type(self.table.item(index, 0)),
                                     NAME=self.check_type(self.table.item(index, 1)),
                                     OBJSIGN=self.check_type(self.table.item(index, 6)),
                                     KLASSNAME=self.check_type(self.table.item(index, 2)),
                                     EVKLASSNAME=self.check_type(self.table.item(index, 3)),
                                     PLCNAME=self.check_type(self.table.item(index, 4)),
                                     PLC_ADRESS=self.check_type(self.table.item(index, 5)))))

            f.write(template.render(vars=contents))

    def check_type(self, data):
        return '' if type(data) == type(None) else data.text()
