# -*- coding: cp1251 -*-
import xml.dom.minidom
from collections import namedtuple
from datetime import datetime

from PyQt5.QtWidgets import *
from jinja2 import BaseLoader
from jinja2 import Environment, FileSystemLoader

from LybPyQT5.widgets.button import SimpleBtn
from LybPyQT5.widgets.tab import LibTab
from LybPyQT5.widgets.table import TableSimple
from LybPyQT5.widgets.text_editor import TextEditor

row_data = namedtuple('row_data', 'kadr evklass main')


class Tab(LibTab):
    def __init__(self):
        super().__init__()
        self.rows = []
        self.initData()
        self.initUI()

    def initData(self):
        self.rows = []
        self.main_title = None

    def initUI(self):

        self.table = TableSimple(name=
            ["MARKA", "NAME", "KLASSNAME", "EVKLASSNAME", "PLCNAME", "PLC_ADRESS", "OBJSIGN"])

        button_open = SimpleBtn(label="������� xml", click_func=self.open_xml)
        button_except = SimpleBtn(label="��������", click_func=self.tab_view)
        button_clean = SimpleBtn(label="��������", click_func=self.table_clean)
        button_generat = SimpleBtn(label="�������������", click_func=self.gerait_xml)
        button_open_example = SimpleBtn(label="���������� ������", click_func=self.open_example_xml)

        self.xml_template = QLabel("None")
        self.xml_template.setWordWrap(True)

        self.text_panel = TextEditor(
            text="""[dict(MARKA=f"GP0011_SPPV_{item1}", NAME=f"{item2}", OBJSIGN=f"P", KLASSNAME="[���]\�������������\��0011 ����", EVKLASSNAME="[��� ���������������]\�������������\��0011 ����", PLCNAME="ICore_2") for item1, item2 in [["K12_WORK", "������"], ["K12_ALARM", "������"],["K13_WORK", "������"], ["K13_ALARM", "������"]]]""",
            height=200)

        self.main_layout.addWidget(self.table, 0, 0, 27, 1)
        self.main_layout.addWidget(self.text_panel, 27, 0, 1, 1)
        self.main_layout.addWidget(self.xml_template, 12, 2, 1, 2)

        self.main_layout.addWidget(button_clean, 15, 3, 1, 1)
        self.main_layout.addWidget(button_except, 15, 2, 1, 1)
        self.main_layout.addWidget(button_open, 14, 2, 1, 2)
        self.main_layout.addWidget(button_open_example, 6, 2, 1, 2)

        self.main_layout.addWidget(button_generat, 27, 2, 1, 2)


    def table_clean(self):
        self.table.setRowCount(1)

    def tab_view(self):
        connection = eval(self.text_panel.toPlainText())
        for conn in connection:
            index = self.table.rowCount()
            self.table.setRowCount(index + 1)  # � ���� ������ � �������
            self.table.setRowHeight(index, 50)

            # self.table.setCellWidget(index, 0, widj_tab1.lineWap(conn.get('MARKA', '')))
            self.table.setItem(index, 0, QTableWidgetItem(conn.get('MARKA', '')))
            self.table.setItem(index, 1, QTableWidgetItem(conn.get('NAME', '')))
            self.table.setItem(index, 2, QTableWidgetItem(conn.get('KLASSNAME', '')))
            self.table.setItem(index, 3, QTableWidgetItem(conn.get('EVKLASSNAME', '')))
            self.table.setItem(index, 4, QTableWidgetItem(conn.get('PLCNAME', '')))
            self.table.setItem(index, 5, QTableWidgetItem(conn.get('PLC_ADRESS', '')))
            self.table.setItem(index, 6, QTableWidgetItem(conn.get('OBJSIGN', '')))
        self.table.resizeRowsToContents()

    def open_xml(self):
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        path, _ = QFileDialog.getOpenFileName(self, '������� xml', "", "Xml (*.xml)", options=options)

        if path == '':
            return

        with open(path, "r", encoding='UTF-8') as f:
            # contents = f.read()#.encode().decode('utf-8')
            dom = xml.dom.minidom.parse(path)
            dom.normalize()
            itemlist = dom.getElementsByTagName('TEHOBJ')
            for item in itemlist:
                item.attributes['MARKA'].value = "{{MARKA}}"
                item.attributes['EVKLASSNAME'].value = "{{EVKLASSNAME}}"
                item.attributes['KLASSNAME'].value = "{{KLASSNAME}}"
                item.attributes['NAME'].value = "{{NAME}}"
                item.attributes['PLCNAME'].value = "{{PLCNAME}}"
                item.attributes['OBJSIGN'].value = "{{OBJSIGN}}"
                item.attributes['PLC_ADRESS'].value = "{{PLC_ADRESS}}"

            now = datetime.now()
            self.xml_template.setText(path + '\n' + str(now.hour) + ':' + str(now.minute) + ':' + str(now.second))

            self.template_t = dom.toxml()
            self.template_t = self.template_t.replace('<?xml version="1.0" ?><root>', '')
            self.template_t = self.template_t.replace('</root>', '')


    def open_example_xml(self):
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        path, _ = QFileDialog.getOpenFileName(self, '������� xml', "", "Xml (*.xml)", options=options)

        if path == '':
            return

        with open(path, "r", encoding='UTF-8') as f:
            # contents = f.read()#.encode().decode('utf-8')
            dom = xml.dom.minidom.parse(path)
            dom.normalize()
            itemlist = dom.getElementsByTagName('TEHOBJ')
            self.table.setRowCount(0)  # � ���� ������ � �������
            for item in itemlist:
                index = self.table.rowCount()
                self.table.setRowCount(index + 1)  # � ���� ������ � �������
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

    def gerait_xml(self):
        try:
            template1 = Environment(loader=BaseLoader).from_string(self.template_t)
            env = Environment(loader=FileSystemLoader('.'))
            template = env.get_template('templates/tab2/main_.html')
            contents = []
            # connection = eval(self.text_panel.toPlainText())
            options = QFileDialog.Options()
            # options |= QFileDialog.DontUseNativeDialog
            fileName, _ = QFileDialog.getSaveFileName(self, "��������� xml", "", "xml (*.xml)", options=options)

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
        except Exception as e:
            self.text_panel.setText('Error')
            QMessageBox().warning(self, "������", str(e), QMessageBox.Ok,
                                  QMessageBox.Ok)

    def check_type(self, data):
        return '' if type(data) == type(None) else data.text()
