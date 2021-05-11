# -*- coding: cp1251 -*-
import collections
import os
import xml.dom.minidom
from collections import namedtuple
from datetime import datetime

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from bs4 import BeautifulSoup
from jinja2 import BaseLoader
from jinja2 import Environment, FileSystemLoader
from jinja2 import meta

from LybPyQT5.widgets.button import SimpleBtn
from LybPyQT5.widgets.check_box import CheckBox
from LybPyQT5.widgets.label import SimpleLabel
from LybPyQT5.widgets.line_text import LineLabel
from LybPyQT5.widgets.tab import LibTab
from LybPyQT5.widgets.table import TableSimple
from LybPyQT5.widgets.text_editor import TextEditor

row_data = namedtuple('row_data', 'kadr evklass main')


def roundUpToMultiple(number, multiple):
    num = number + (multiple - 1)
    return num - (num % multiple)


class Template:

    def open_xml(self, path):
        self.maximum_x = 0
        self.maximum_y = 0

        self.atr_dict = {}
        self.dict_param = {}

        with open(path, "r", encoding='UTF-8') as f:
            # contents = f.read()#.encode().decode('utf-8')
            dom = xml.dom.minidom.parse(path)
            dom.normalize()
            itemlist = dom.getElementsByTagName('OnePrim')
            for item in itemlist:
                if self.maximum_x < int(item.attributes['X'].value) + int(item.attributes['WIDTH'].value):
                    self.maximum_x = int(item.attributes['X'].value) + int(item.attributes['WIDTH'].value)

                if self.maximum_y < int(item.attributes['Y'].value) + int(item.attributes['HEIGHT'].value):
                    self.maximum_y = int(item.attributes['Y'].value) + int(item.attributes['HEIGHT'].value)

                item.attributes['X'].value = "{{dict.X + %s}}" % (item.attributes['X'].value)
                item.attributes['Y'].value = "{{dict.Y + %s}}" % (item.attributes['Y'].value)

            ind = 1
            itemlist = dom.getElementsByTagName('CardExDATA')
            for item in itemlist:
                if item.firstChild.data in self.dict_param.keys():
                    item.firstChild.data = self.dict_param[item.firstChild.data]
                else:
                    self.dict_param[item.firstChild.data] = "{{dict.CardExDATA_%s}}" % ind
                    self.atr_dict["CardExDATA_%s" % ind] = item.firstChild.data
                    item.firstChild.data = "{{dict.CardExDATA_%s}}" % ind
                    ind += 1

            itemlist = dom.getElementsByTagName('PARAMS')
            for item in itemlist:
                list_str = []
                if item.firstChild.data.find('[PL]=') != -1:
                    asr = item.firstChild.data.split(';')
                    for s in asr:
                        if s.find('(') == -1:
                            break

                        x, y = s[s.find("(") + 1:s.find(")")].split(',')
                        list_str.append('({{dict.X + %s}},{{dict.Y + %s}});' % (x, y))

                    slovo = ''.join(list_str)
                    params = f"""[PL]={slovo}
                [HINT]="""
                    item.firstChild.data = params

                if item.firstChild.data.find('[TEXT]=') != -1:
                    others_param = item.firstChild.data.split('\n')
                    for index_insert, paramentrs in enumerate(others_param):
                        if paramentrs.find('[TEXT]=') != -1:
                            text_str = others_param.pop(index_insert)
                            break

                    if len(''.join(text_str.split())) != len('[TEXT]='):
                        param_text = text_str[len('[TEXT]='):len(text_str)]
                        if param_text in self.dict_param.keys():
                            text_str = self.dict_param[item.attributes['EXDATA'].value]
                        else:
                            self.dict_param[param_text] = "{{dict.CardExDATA_%s}}" % ind
                            self.atr_dict["CardExDATA_%s" % ind] = param_text
                            text_str = "[TEXT]={{dict.CardExDATA_%s}}" % ind
                            ind += 1
                        others_param.insert(index_insert, text_str)
                        item.firstChild.data = '\n'.join(others_param)

            itemlist = dom.getElementsByTagName('OneReceptor')
            for item in itemlist:
                if item.attributes['EXDATA'].value in self.dict_param.keys():
                    item.attributes['EXDATA'].value = self.dict_param[item.attributes['EXDATA'].value]
                else:
                    self.dict_param[item.attributes['EXDATA'].value] = "{{dict.CardExDATA_%s}}" % ind
                    self.atr_dict["CardExDATA_%s" % ind] = item.attributes['EXDATA'].value
                    item.attributes['EXDATA'].value = "{{dict.CardExDATA_%s}}" % ind
                    ind += 1

            itemlist = dom.getElementsByTagName('OneAnim')
            for item in itemlist:
                for animators in item.getElementsByTagName('ExData'):
                    if animators.firstChild.data in self.dict_param.keys():
                        animators.firstChild.data = self.dict_param[animators.firstChild.data]
                    else:
                        self.dict_param[animators.firstChild.data] = "{{dict.CardExDATA_%s}}" % ind
                        self.atr_dict["CardExDATA_%s" % ind] = animators.firstChild.data
                        animators.firstChild.data = "{{dict.CardExDATA_%s}}" % ind
                        ind += 1

            self.template_t = dom.toxml()

            soup = BeautifulSoup(self.template_t, 'xml')

            self.new_file = list(map(str, soup.find_all('OnePrim')))
            self.new_file = ''.join(self.new_file)

    def save_to_file(self, path):
        with open(path, "w", encoding="UTF-8") as file:
            file.write(self.new_file)

    def get_tempalte(self, path):
        with open(path, "r", encoding='UTF-8') as f:
            self.new_file = f.readlines()
        self.new_file = ''.join(self.new_file)

        env = Environment(loader=FileSystemLoader(os.path.dirname(path)))
        template_source = env.loader.get_source(env, os.path.basename(path))[0]
        template_source = template_source.replace('dict.', '')
        parsed_content = env.parse(template_source)

        list_atrib = list(meta.find_undeclared_variables(parsed_content))
        list_atrib.remove('X')
        list_atrib.remove('Y')
        # list_atrib.sort()
        list_atrib = sorted(list_atrib, key=lambda x: (len(x), x))
        self.atr_dict = {}
        for atr in list_atrib:
            self.atr_dict[atr] = 'None'

        # Render template without passing all variables


class Tab(LibTab):
    def __init__(self):
        super().__init__()
        self.new_templates = Template()
        self.rows = []
        self.initData()
        self.initUI()

    def initData(self):
        self.rows = []
        self.main_title = None

    def initUI(self):

        self.table = TableSimple(name=["MARKA"])
        # self.table.setSelectionBehavior(QAbstractItemView.SelectItems)  # Выделяет всю строку

        self.table_for_test = TableSimple(name=["SOMETHING"])
        #
        # self.table_for_test.setMaximumWidth(500)

        button_open = SimpleBtn(label="Открыть исх. файл", click_func=self.open_xml)
        button_open_teml = SimpleBtn(label="Открыть шаблон", click_func=self.get_tempalte)
        button_save_teml = SimpleBtn(label="Сохранить шаблон", click_func=self.save_template)

        self.count_element = LineLabel(label="Кол-во в ряду/строке", number='20')
        self.dx = LineLabel(label="dx", number='100')
        self.dy = LineLabel(label="dy ", number='100')

        button_generat = SimpleBtn(label="Сгенерировать", click_func=self.gerait_xml)
        self.xml_template = SimpleLabel(text="None", WordWrap=True)

        self.table.setMaximumWidth(1700)
        self.table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.text_panel = TextEditor(objectName="text1", tooltip='Правила вставки',
                                     text="""[f"2/PLC_GP_21_1BR/1/{str(item1).rjust(2,'0')}/DI_DIG_3A" for item1 in range(1, 3)]""")

        self.offset = CheckBox(label='Смещение по оси x', value=True)

        self.buff_copy = CheckBox(label='Буффер', value=False)

        button_generat_tab2 = SimpleBtn(label="get_table2", click_func=self.generate_table2)

        self.xml_template = SimpleLabel(text="None", WordWrap=True)

        splitter_v = QSplitter(Qt.Vertical)
        splitter_v.addWidget(self.table_for_test)
        splitter_v.addWidget(self.text_panel)

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.table)
        splitter.addWidget(splitter_v)

        self.main_layout.addWidget(splitter, 0, 0, 27, 2)

        self.main_layout.addWidget(button_generat, 23, 2, 1, 2)
        self.main_layout.addWidget(button_generat_tab2, 5, 2, 1, 2)
        self.main_layout.addWidget(self.xml_template, 1, 2, 1, 2)

        self.main_layout.addWidget(button_open_teml, 16, 2, 1, 2)
        self.main_layout.addWidget(button_save_teml, 15, 2, 1, 2)
        self.main_layout.addWidget(button_open, 14, 2, 1, 2)

        self.main_layout.addWidget(self.count_element, 9, 2, 1, 2)
        self.main_layout.addWidget(self.dx, 11, 2, 1, 2)
        self.main_layout.addWidget(self.dy, 12, 2, 1, 2)
        self.main_layout.addWidget(self.offset, 8, 2, 1, 2)
        self.main_layout.addWidget(self.buff_copy, 7, 2, 1, 2)

    def table_clean(self):
        self.table.setRowCount(0)

    def tab_view(self):
        # exec(f'connection = {self.text_panel.toPlainText()}')
        # connection = eval('[dict(MARKA=f"GP0011_SPPV_{item1}_P", NAME=f"{item2}",OBJSIGN=f"P",KLASSNAME="[ВСЕ]\Водоснабжение\ГП0011 СППВ",EVKLASSNAME="[Все технологические]\Водоснабжение\ГП0011 СППВ", PLCNAME="ICore_2") for item1, item2 in [["TO_K1", "Давление на входе насоса K1"],["FROM_K1", "Рабочее давление K1"],["TO_K8", "Давление на входе насоса K8"],["FROM_K8", "Рабочее давление K8"],["TO_K10", "Давление на входе насоса K10"],["FROM_K10", "Рабочее давление K10"],["TO_K14", "Давление на входе насоса K14"],["FROM_K14","Рабочее давление K14"]]]')
        # connection = eval(self.text_panel.toPlainText())
        pass

    def open_xml(self):
        try:
            options = QFileDialog.Options()
            # options |= QFileDialog.DontUseNativeDialog
            path, _ = QFileDialog.getOpenFileName(self, 'Открыть xml', "", "Xml (*.xml)", options=options)

            if path == '':
                return

            with open(path, "r", encoding='UTF-8') as f:
                self.new_templates.open_xml(path)
                self.table_view_set()

            self.watch_path(path)
            self.dx.line_edit.setText(str(roundUpToMultiple(self.new_templates.maximum_x, 50)))
            self.dy.line_edit.setText(str(roundUpToMultiple(self.new_templates.maximum_y, 50)))

        except Exception as e:
            QMessageBox().warning(self, "Ошибка", str(e), QMessageBox.Ok, QMessageBox.Ok)

    def table_view_set(self):
        self.table.setColumnCount(len(self.new_templates.atr_dict.keys()) + 1)  # Устанавливаем три колонки
        labels_list = ['№']
        labels_list.extend(list(self.new_templates.atr_dict.keys()))
        self.table.setHorizontalHeaderLabels(labels_list)
        self.table.setRowCount(1)  # и одну строку в таблице
        header = self.table.horizontalHeader()
        self.table.setItem(0, 0, QTableWidgetItem('1'))
        for in_col, key in enumerate(list(self.new_templates.atr_dict.keys())):
            self.table.setItem(0, in_col + 1, QTableWidgetItem(str(self.new_templates.atr_dict[key])))
            header.setSectionResizeMode(in_col + 1, QHeaderView.Stretch)  # Stretch)
        self.table.setWordWrap(True)

    def gerait_xml(self):
        try:
            template1 = Environment(loader=BaseLoader).from_string(self.new_templates.new_file)
            env = Environment(loader=FileSystemLoader('.'))
            template = env.get_template('templates/tab10/temlate.html')
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
                count_element_max = int(self.count_element.line_edit.text())
                x0 = 0
                y0 = 0
                x = x0
                y = y0
                dx = int(self.dx.line_edit.text())
                dy = int(self.dy.line_edit.text())

                list_atrib = ['X', 'Y']
                list_atrib.extend(list(self.new_templates.atr_dict.keys()))
                dicr_atr = collections.namedtuple('dicr_atr', list_atrib)
                links = []
                count = self.table.rowCount()
                index_row = 1
                for index in range(count):

                    at = [self.table.item(index, col).text() for col in range(1, self.table.columnCount())]
                    my_dict = dicr_atr(x, y, *at)
                    links.append(str(template1.render(dict=my_dict)))

                    if self.offset.isChecked():
                        x += dx
                        if index_row >= count_element_max:
                            x = x0
                            y += dy
                            index_row = 0
                    else:
                        y += dy
                        if index_row >= count_element_max:
                            y = y0
                            x += dx
                            index_row = 0

                    index_row += 1

                f.write(template.render(contents=links))
        except Exception as e:
            self.table_for_test.setItem(0, 0, "Что-то не так")
            QMessageBox().warning(self, "Ошибка", str(e), QMessageBox.Ok, QMessageBox.Ok)

    def check_type(self, data):
        return '' if type(data) == type(None) else data.text()

    def generate_table2(self):
        self.table_for_test.setRowCount(0)
        try:
            connection = eval(self.text_panel.toPlainText())
            for conn in connection:
                index = self.table_for_test.rowCount()
                self.table_for_test.setRowCount(index + 1)  # и одну строку в таблице
                self.table_for_test.setRowHeight(index, 50)
                self.table_for_test.setItem(index, 0, QTableWidgetItem(conn))
            self.table_for_test.resizeRowsToContents()
        except Exception as e:
            self.table_for_test.setRowCount(1)
            self.table_for_test.setItem(0, 0, "Что-то не так")
            QMessageBox().warning(self, "Ошибка", str(e), QMessageBox.Ok, QMessageBox.Ok)

    def save_template(self):
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "Сохранить xml", "", "xml (*.xml)", options=options)

        if fileName == '':
            return

        if fileName.find('.xml') == -1:
            fileName += '.xml'

        try:
            self.new_templates.save_to_file(fileName)
        except Exception as e:
            self.error_message()
            QMessageBox().warning(self, "Ошибка", str(e), QMessageBox.Ok, QMessageBox.Ok)

    def get_tempalte(self):
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        path, _ = QFileDialog.getOpenFileName(self, 'Открыть xml', "", "Xml (*.xml)", options=options)

        if path == '':
            return

        try:
            self.new_templates.get_tempalte(path)
            self.table_view_set()
            self.watch_path(path)
        except Exception as e:
            self.error_message()
            QMessageBox().warning(self, "Ошибка", str(e), QMessageBox.Ok, QMessageBox.Ok)

    def error_message(self):
        self.xml_template.setText("Ошибка! :(")

    def watch_path(self, path):
        now = datetime.now()
        self.xml_template.setText(path + '\n' + str(now.hour) + ':' + str(now.minute) + ':' + str(now.second))
