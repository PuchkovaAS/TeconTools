# -*- coding: cp1251 -*-
import collections
import os
import xml.dom.minidom
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


def roundUpToMultiple(number, multiple):
    num = number + (multiple - 1)
    return num - (num % multiple)


class Template:

    def links(self, dom):
        itemlist = dom.getElementsByTagName('PointList')
        for item in itemlist:
            list_str = []

            asr = item.getAttribute("PL").split(';')
            for s in asr:
                if s.find('(') == -1:
                    break

                x, y = s[s.find("(") + 1:s.find(")")].split(',')
                list_str.append('({{dict.X + %s}},{{dict.Y + %s}});' % (x, y))

            slovo = ''.join(list_str)
            params = f'''{slovo}'''
            item.setAttribute("PL", params)

        itemlist = dom.getElementsByTagName('LastPoint')
        for item in itemlist:
            asr = item.getAttribute("LP").split('|')
            asr[0] = '{{dict.index + %s}}' % (asr[0])
            params = f'''{'|'.join(asr)}'''
            item.setAttribute("LP", params)

        itemlist = dom.getElementsByTagName('FirstPoint')
        for item in itemlist:
            asr = item.getAttribute("FP").split('|')
            asr[0] = '{{dict.index + %s}}' % (asr[0])
            params = f'''{'|'.join(asr)}'''
            item.setAttribute("FP", params)

    def bloks(self, dom):
        self.maximum_x = 0
        self.maximum_y = 0

        maximum = None
        minimum = None

        self.atr_dict = {}
        dict_param = {}

        itemlist = dom.getElementsByTagName('Block')
        for item in itemlist:
            ident = int(item.getAttribute("T11ID"))
            if maximum is None or maximum < ident:
                maximum = ident

            if minimum is None or minimum > ident:
                minimum = ident

            item.setAttribute("T11ID", '{{dict.index + %s}}' % ident)

            param = item.getAttribute("Info").split('.')
            if param[0] in self.atr_dict.keys():
                name = dict_param[item.getAttribute("Info")]
            else:
                name = f'Info{len(self.atr_dict) + 1}'
                self.atr_dict[name] = param[0]
                dict_param[param[0]] = name

            if len(param) > 1:
                item.setAttribute("Info", '{{dict.%s}}.%s' % (name, param[1]))
            else:
                item.setAttribute("Info", '{{dict.%s}}' % (name))

        itemlist = dom.getElementsByTagName('Graphics')
        for item in itemlist:

            if self.maximum_x < int(item.getAttribute("X")) + int(item.getAttribute("WIDTH")):
                self.maximum_x = int(item.getAttribute("X")) + int(item.getAttribute("WIDTH"))

            if self.maximum_y < int(item.getAttribute("Y")) + int(item.getAttribute("HEIGHT")):
                self.maximum_y = int(item.getAttribute("Y")) + int(item.getAttribute("HEIGHT"))

            item.setAttribute("X", '{{dict.X + %s}}' % (item.getAttribute("X")))
            item.setAttribute("Y", '{{dict.Y + %s}}' % (item.getAttribute("Y")))

        self.num_of_index = 1
        itemlist = dom.getElementsByTagName('Params')
        for item in itemlist:
            try:
                name = dict_param[item.getAttribute("Instance")]
                item.setAttribute("Instance", '{{dict.%s}}' % (name))
            except:
                pass
            self.num_of_index += 1

        self.delta = maximum - minimum

    def open_xml(self, path):

        with open(path, "r", encoding='UTF-8') as f:
            contents = f.read()
            contents = contents.replace('', '')
            dom = xml.dom.minidom.parseString(contents)
            dom.normalize()

            self.links(dom)

            self.bloks(dom)

            self.template_t = dom.toxml()

            soup = BeautifulSoup(self.template_t, 'xml')
            new_1 = list(map(str, soup.find_all('Block')))
            self.bloks_data = ''.join(new_1)
            # with open("output1.xml", "w", encoding="UTF-8") as file:
            #     file.write(new_1)

            new_2 = list(map(str, soup.find_all('Link')))
            self.links_data = ''.join(new_2)
            # with open("output2.xml", "w", encoding="UTF-8") as file:
            #     file.write(self.links_data)
            # dom.writexml(open(fileName, 'w'))
            #
            # with open(fileName, 'w') as file:
            #     file.write(self.template_t)

    def save_to_file(self, path):
        env = Environment(loader=FileSystemLoader('.'))
        template = env.get_template('templates/tab11/for_templ.html')

        with open(path, "w", encoding='utf8') as f:
            f.write(template.render(block=self.bloks_data, link=self.links_data, delta=self.delta))

    def get_tempalte(self, path):
        with open(path, "r", encoding='UTF-8') as f:
            contents = f.readlines()
        contents = ''.join(contents)
        dom = xml.dom.minidom.parseString(contents)
        dom.normalize()
        self.template_t = dom.toxml()
        soup = BeautifulSoup(self.template_t, 'xml')

        for group in dom.getElementsByTagName('Delta'):
            self.delta = int(group.childNodes[0].data)

        new_1 = list(map(str, soup.find_all('Block')))
        self.bloks_data = ''.join(new_1)
        new_1 = list(map(str, soup.find_all('Link')))
        self.links_data = ''.join(new_1)

        env = Environment(loader=FileSystemLoader(os.path.dirname(path)))
        template_source = env.loader.get_source(env, os.path.basename(path))[0]
        template_source = template_source.replace('dict.', '')
        parsed_content = env.parse(template_source)

        list_atrib = list(meta.find_undeclared_variables(parsed_content))
        list_atrib.remove('X')
        list_atrib.remove('Y')
        list_atrib.remove('index')
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
        # self.table_for_test.setSelectionBehavior(QAbstractItemView.SelectItems)  # Выделяет всю строку
        # self.table_for_test.setMaximumWidth(500)

        button_open = SimpleBtn(label="Открыть исх. файл", click_func=self.open_xml)

        self.count_element = LineLabel(label="Кол-во в ряду/строке", number='20')
        self.dx = LineLabel(label="dx", number='100')
        self.dy = LineLabel(label="dy ", number='100')

        button_generat = SimpleBtn(label="Сгенерировать", click_func=self.gerait_xml)
        button_open_teml = SimpleBtn(label="Открыть шаблон", click_func=self.get_tempalte)
        button_save_teml = SimpleBtn(label="Сохранить шаблон", click_func=self.save_template)

        self.xml_template = SimpleLabel(text="None", WordWrap=True)

        self.table.setMaximumWidth(1700)
        self.table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.text_panel = TextEditor(objectName="text1", tooltip='Правила вставки',
                                     text="""[f"2/PLC_GP_21_1BR/1/{str(item1).rjust(2,'0')}/DI_DIG_3A" for item1 in range(1, 3)]""")

        self.offset = CheckBox(label='Смещение по оси x', value=True)

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

        self.main_layout.addWidget(button_open, 14, 2, 1, 2)
        self.main_layout.addWidget(button_open_teml, 16, 2, 1, 2)
        self.main_layout.addWidget(button_save_teml, 15, 2, 1, 2)

        self.main_layout.addWidget(self.count_element, 9, 2, 1, 2)
        self.main_layout.addWidget(self.dx, 11, 2, 1, 2)
        self.main_layout.addWidget(self.dy, 12, 2, 1, 2)
        self.main_layout.addWidget(self.offset, 8, 2, 1, 2)

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
            QMessageBox().warning(self, "Ошибка", str(e), QMessageBox.Ok,
                                  QMessageBox.Ok)

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
            QMessageBox().warning(self, "Ошибка", str(e), QMessageBox.Ok,
                                  QMessageBox.Ok)

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

        try:
            with open(path, "r", encoding='UTF-8') as f:
                self.new_templates.open_xml(path)
                self.table_view_set()

            self.watch_path(path)
            self.dx.line_edit.setText(str(roundUpToMultiple(self.new_templates.maximum_x, 50)))
            self.dy.line_edit.setText(str(roundUpToMultiple(self.new_templates.maximum_y, 50)))

        except Exception as e:
            self.error_message()
            QMessageBox().warning(self, "Ошибка", str(e), QMessageBox.Ok,
                                  QMessageBox.Ok)

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
            bloks_templ = Environment(loader=BaseLoader).from_string(self.new_templates.bloks_data)
            links_templ = Environment(loader=BaseLoader).from_string(self.new_templates.links_data)
            env = Environment(loader=FileSystemLoader('.'))
            template = env.get_template('templates/tab11/main.html')

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

                list_atrib = ['X', 'Y', 'index']
                list_atrib.extend(list(self.new_templates.atr_dict.keys()))
                dicr_atr = collections.namedtuple('dicr_atr', list_atrib)
                links = []
                count = self.table.rowCount()
                index_of_element = 0
                bloks = []
                index_row = 1
                for index in range(count):

                    at = [self.table.item(index, col).text() for col in range(1, self.table.columnCount())]
                    my_dict = dicr_atr(x, y, index_of_element, *at)
                    links.append(str(links_templ.render(dict=my_dict)))
                    bloks.append(str(bloks_templ.render(dict=my_dict)))
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
                    index_of_element += self.new_templates.delta + 1
                f.write(template.render(bloks=bloks, links=links))
        except Exception as e:
            self.text_panel.setText('Что-то пошло не так')
            QMessageBox().warning(self, "Ошибка", str(e), QMessageBox.Ok,
                                  QMessageBox.Ok)

    @staticmethod
    def check_type(data):
        return '' if isinstance(data, type(None)) else data.text()

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
            QMessageBox().warning(self, "Ошибка", str(e), QMessageBox.Ok,
                                  QMessageBox.Ok)

    def watch_path(self, path):
        now = datetime.now()
        self.xml_template.setText(path + '\n' + str(now.hour) + ':' + str(now.minute) + ':' + str(now.second))

    def error_message(self):
        self.xml_template.setText("Ошибка! :(")
