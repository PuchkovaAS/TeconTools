import copy
from collections import namedtuple
from functools import partial

from PyQt5 import QtGui
from PyQt5.QtCore import QLine
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QPushButton, QHBoxLayout
import xml.etree.cElementTree as ET
from bs4 import BeautifulSoup
import lxml.etree as etree
import xml.dom.minidom

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
        self.table = widj_tab1.table_setting(["Кадр", "Группа", "Уровень"])
        self.button_add_row = widj_tab1.button_setting("Добавить строку", self.table_add)
        self.button_del_row = widj_tab1.button_setting("Удалить строку", self.table_del)
        self.button_upper = widj_tab1.button_setting("Вверх", partial(self.move_to, -1))
        self.button_lower = widj_tab1.button_setting("Вниз", partial(self.move_to, 1))
        button_to_main = widj_tab1.button_setting("Создать файл импорта", self.generate_menu)
        button_save = widj_tab1.button_setting("Сохранить шаблон", self.save_xml_el)
        button_open = widj_tab1.button_setting("Открыть шаблон", self.read_xml_el)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)  # ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)  # Выделяет всю строку

        self.table1 = widj_tab1.table_setting(["Кадр", "Группа", "Уровень"])
        self.table1.setRowCount(1)  # и одну строку в таблице
        self.table1.setFixedHeight(50)
        self.table1.horizontalHeader().hide()


        self.main_title = [widj_tab1.line_btn(1, 1, self), widj_tab1.line_btn(1, 2, self), widj_tab1.qbox_line(),
                           widj_tab1.check_box(self, 0)]
        self.table1.setRowHeight(0, 50)
        self.table1.setCellWidget(0, 1, self.main_title[0])
        self.table1.setCellWidget(0, 0, self.main_title[1])
        self.table1.setCellWidget(0, 2, self.main_title[2])

        main_layout.addWidget(self.table, 0, 0, 27, 1)
        main_layout.addWidget(self.table1, 27, 0, 1, 1)

        main_layout.addWidget(self.button_add_row, 1, 2, 1, 2)
        main_layout.addWidget(self.button_del_row, 2, 2, 1, 2)
        main_layout.addWidget(self.button_upper, 3, 2, 1, 1)
        main_layout.addWidget(self.button_lower, 3, 3, 1, 1)

        self.width = widj_tab1.lile_label("Ширина", '274')
        self.width_screen = widj_tab1.lile_label("Ширина окна", '1920')
        self.indent = widj_tab1.lile_label("Отступ ", '5')

        self.check_box_line = widj_tab1.check_box_line("Нижний фрейм")
        self.check_box_line.cb.stateChanged.connect(self.hideTable)

        self.edict = widj_tab1.line_botton_switch("Импорт из БД", "Импрортировать")
        self.edict.btn.clicked.connect(self.create_table1)

        main_layout.addWidget(self.check_box_line, 4, 2, 1, 2)
        main_layout.addWidget(self.edict, 5, 2, 1, 2)

        main_layout.addWidget(self.width_screen, 12, 2, 1, 2)
        main_layout.addWidget(self.width, 13, 2, 1, 2)
        main_layout.addWidget(self.indent, 14, 2, 1, 2)

        main_layout.addWidget(button_to_main, 26, 2, 1, 2)

        main_layout.addWidget(button_save, 27, 2, 1, 1)
        main_layout.addWidget(button_open, 27, 3, 1, 1)
        main_layout.addWidget(widj_tab1.line_btn(2, 1, self), 0, 2, 1, 2)

        self.hide_all()

        self.setLayout(main_layout)

    def hide_all(self):
        self.edict.hide()
        self.button_add_row.hide()
        self.button_del_row.hide()
        self.button_lower.hide()
        self.button_upper.hide()

    def show_all(self):
        self.edict.show()
        self.button_add_row.show()
        self.button_del_row.show()
        self.button_lower.show()
        self.button_upper.show()

    def create_table1(self):
        try:
            main_kadr = self.main_title[1].line_text.text().split('/')[-1]
            main_evklass = self.main_title[0].line_text.text().split('/')[-1]
            cur = self.con.cursor()

            select = f"select ID from GRPAGES WHERE name = '{main_kadr}'"
            cur.execute(select)
            main_PID_kadr = [pid[0] for pid in cur][0]

            select = f"select ID from EVKLASSIFIKATOR WHERE name = '{main_evklass}'"
            cur.execute(select)
            main_PID_evklass = [pid[0] for pid in cur][0]

            select = f"select NAME from EVKLASSIFIKATOR WHERE PID = {main_PID_evklass} order by name"
            cur.execute(select)
            evklass_list = [self.main_title[0].line_text.text() + '/' + name[0] for name in cur]

            select = f"select NAME from GRPAGES WHERE PID = {main_PID_kadr} order by name"
            cur.execute(select)
            grapages_list = [self.main_title[1].line_text.text() + '/' + name[0] for name in cur]

            self.rows.clear()
            for index in range(len(grapages_list)):
                self.table.setRowCount(index + 1)  # и одну строку в таблице
                self.rows.append([widj_tab1.line_btn(1, 1, self), widj_tab1.line_btn(1, 2, self), widj_tab1.qbox_line(),
                                  widj_tab1.check_box(self, index)])
                self.table.setRowHeight(index, 50)

                if len(evklass_list) > index:
                    self.rows[-1][0].line_text.setText(evklass_list[index])

                if len(grapages_list) > index:
                    self.rows[-1][1].line_text.setText(grapages_list[index])

                self.table.setCellWidget(index, 1, self.rows[-1][0])
                self.table.setCellWidget(index, 0, self.rows[-1][1])
                self.table.setCellWidget(index, 2, self.rows[-1][2])

            self.table.setRowCount(len(self.rows))
        except Exception as e:
            QMessageBox().warning(self, "Ошибка", str(e)+'\n Ошибка подлючения к базе', QMessageBox.Ok, QMessageBox.Ok)

    def hideTable(self):
        if self.check_box_line.cb.checkState():
            self.table1.hide()
            self.edict.hide()
            self.table.hideColumn(2)
        else:
            self.table1.show()
            self.edict.show()
            self.table.showColumn(2)

    def move_to(self, direction):

        selected_row = self.table.selectedRanges()[0].topRow()
        self.rows[selected_row], self.rows[selected_row + direction] = self.rows[selected_row + direction], self.rows[
            selected_row]

        kadr, evkalss, level = self.prepare_move()
        self.rows.clear()

        self.table.setRowCount(len(kadr))  # и одну строку в таблице

        for index in range(len(kadr)):
            self.table.setRowCount(index + 1)  # и одну строку в таблице
            self.rows.append([widj_tab1.line_btn(1, 1, self), widj_tab1.line_btn(1, 2, self), widj_tab1.qbox_line(),
                              widj_tab1.check_box(self, index)])
            self.table.setRowHeight(index, 50)
            self.rows[-1][0].line_text.setText(evkalss[index])
            self.rows[-1][1].line_text.setText(kadr[index])
            self.rows[-1][2].cb.setCurrentText(str(level[index]))

            self.table.setCellWidget(index, 1, self.rows[-1][0])
            self.table.setCellWidget(index, 0, self.rows[-1][1])
            self.table.setCellWidget(index, 2, self.rows[-1][2])

        self.table.selectRow(selected_row + direction)

    def open_search(self, row, table):
        self.new.show()

    def table_add(self):
        index = self.table.rowCount()
        self.table.setRowCount(index + 1)  # и одну строку в таблице
        self.rows.append([widj_tab1.line_btn(1, 1, self), widj_tab1.line_btn(1, 2, self), widj_tab1.qbox_line(),
                          widj_tab1.check_box(self, index)])
        self.table.setRowHeight(index, 50)
        self.table.setCellWidget(index, 1, self.rows[-1][0])
        self.table.setCellWidget(index, 0, self.rows[-1][1])
        self.table.setCellWidget(index, 2, self.rows[-1][2])

    def table_del(self):
        selected_rows = self.table.selectedRanges()
        sorted_rows = []
        for row in selected_rows:
            sorted_rows.append(row.topRow())
        sorted_rows.sort(reverse=True)
        for row in sorted_rows:
            self.table.removeRow(row)
            self.rows.pop(row)

    def prepare_move(self):
        # окна
        page_name = []
        # группа событий
        evkalss = []
        level = []

        for index in range(self.table.rowCount()):
            evkalss.append(self.rows[index][0].line_text.text())
            page_name.append(self.rows[index][1].line_text.text())
            level.append(int(self.rows[index][2].cb.currentText()))

        return page_name, evkalss, level

    def prepare(self):
        # окна
        page_name = []
        # группа событий
        evkalss = []
        level = []

        for index in range(self.table.rowCount()):
            evkalss.append(self.rows[index][0].line_text.text().split('/')[-1])
            page_name.append(self.rows[index][1].line_text.text().split('/')[-1])
            level.append(int(self.rows[index][2].cb.currentText()))

        return page_name, evkalss, level

    def generate_menu(self):
        page_name, evkalss, level = self.prepare()
        if self.check_box_line.cb.checkState():
            self.generation_screen(page_name, evkalss, level)
        else:
            self.create_file(page_name, evkalss, level)

    def generation_screen(self, page_name, evkalss, level):

        width = int(self.width_screen.line_edit.text()) // len(page_name)

        template_num = []
        env1 = Environment(loader=FileSystemLoader('.'))

        template_num.append(env1.get_template('templates/main_btn/pict.html'))

        template_num.append(env1.get_template('templates/other_btn/other_brn.html'))

        env = Environment(loader=FileSystemLoader('.'))
        template = env.get_template('templates/main_title/main_title.html')

        main_title = self.main_title[1].line_text.text().split('/')[-1]

        vars = []
        pict = []
        pict2 = []
        page = []
        # Шаблоны
        x0 = 0
        grnum = 0

        # Сохраняем
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "Сохранить xml", "", "xml (*.xml)", options=options)

        if fileName == '':
            return

        if fileName.find('.xml') == -1:
            fileName += '.xml'

        with open(fileName, "w", encoding='utf8') as f:
            for index in range(len(page_name)):
                page.append(str(template_num[1].render(name_title=main_title, Y=0, evklass=evkalss[index],
                                                       page_name=page_name[index],
                                                       X=x0,
                                                       WIDTH=width,
                                                       X0=x0)))

                pict2.append(str(template_num[0].render(name_title=evkalss[index], Y=0, GRNUM=grnum, X=x0,
                                                        WIDTH=width,
                                                        X0=x0)))
                x0 += width
                grnum += 4

            f.write(template.render(name_title=main_title, Y=25, others=page, picts2=pict2, vars=vars, picts=pict,
                                    WIDTH=int(self.width_screen.line_edit.text())))

    def create_file(self, page_name, evkalss, level):
        template_num = []
        env1 = Environment(loader=FileSystemLoader('.'))
        template_num.append(env1.get_template('templates/main_btn/main_btn.html'))

        template_num.append(env1.get_template('templates/main_btn/pict.html'))

        template_num.append(env1.get_template('templates/other_btn/other_brn.html'))

        env = Environment(loader=FileSystemLoader('.'))
        template = env.get_template('templates/main_title/main_title.html')

        main_title = self.main_title[1].line_text.text().split('/')[-1]

        vars = []
        contents = []
        pict = []
        pict2 = []
        page = []
        # Шаблоны
        y0 = 0
        grnum = 0
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "Сохранить xml", "", "xml (*.xml)", options=options)

        with open(fileName, "w", encoding='utf8') as f:
            for index in range(len(page_name)):
                page.append(str(template_num[2].render(name_title=main_title, Y=y0, evklass=evkalss[index],
                                                       page_name=page_name[index],
                                                       X=level[index] * int(self.indent.line_edit.text()),
                                                       WIDTH=int(self.width.line_edit.text()),
                                                       X0=0)))
                pict2.append(str(template_num[1].render(name_title=evkalss[index], Y=y0, GRNUM=grnum, X=0,
                                                        WIDTH=int(self.width.line_edit.text()),
                                                        X0=0)))
                y0 += 25
                grnum += 4

            for index in range(1):
                vars.append(str(
                    template_num[0].render(name_title=main_title, Y=y0, X=0, WIDTH=int(self.width.line_edit.text()),
                                           X0=0)))
                pict.append(str(
                    template_num[1].render(name_title=self.main_title[0].line_text.text().split('/')[-1], Y=y0 + 2,
                                           GRNUM=grnum, X=0,
                                           WIDTH=int(self.width.line_edit.text()),
                                           X0=0)))
                y0 += 30
                grnum += 4

            f.write(template.render(name_title=main_title, Y=y0, others=page, picts2=pict2, vars=vars, picts=pict,
                                    WIDTH=int(self.width.line_edit.text())))

    def save_xml_el(self):

        type_block = ET.Element("Type", name=f"{self.main_title[1].line_text.text()}")

        input_block = ET.SubElement(type_block, "main_block")

        ET.SubElement(input_block, f"Main", kadr=f"{self.main_title[1].line_text.text()}",
                      level=f"{self.main_title[2].cb.currentText()}",
                      evklass=self.main_title[0].line_text.text())

        output_block = ET.SubElement(type_block, "others_blocks")

        page_name, evkalss, level = self.prepare()

        for index in range(len(page_name)):
            ET.SubElement(output_block, f"Others", kadr=f"{page_name[index]}",
                          level=f"{level[index]}",
                          evklass=evkalss[index])

        # tree = ET.ElementTree(type_block)

        # Сохраняем
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "Сохранить xml", "", "Xml (*.xml)", options=options)

        if fileName == '':
            return

        if fileName.find('.xml') == -1:
            fileName += '.xml'

        # tree.write(fileName, encoding = "UTF-8", xml_declaration = True)
        xmlstr = ET.tostring(type_block, encoding="UTF-8", method='xml').decode()
        x = etree.fromstring(xmlstr)

        document = open(fileName, 'w+')
        document.write(bytes.decode(etree.tostring(x, pretty_print=True, encoding='UTF-8'), encoding='windows-1251'))
        document.close()

    def read_xml_el(self):
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        path, _ = QFileDialog.getOpenFileName(self, 'Открыть xml', "", "Xml (*.xml)", options=options)

        if path == '':
            return

        with open(path, "r", encoding='UTF-8') as f:
            # contents = f.read()#.encode().decode('utf-8')
            dom = xml.dom.minidom.parse(path)
            dom.normalize()

            itemlist = dom.getElementsByTagName('Main')
            for item in itemlist:
                self.main_title = [widj_tab1.line_btn(1, 1, self), widj_tab1.line_btn(1, 2, self),
                                   widj_tab1.qbox_line(),
                                   widj_tab1.check_box(self, 0)]
                self.main_title[0].line_text.setText(item.attributes['evklass'].value)
                self.main_title[1].line_text.setText(item.attributes['kadr'].value)
                self.main_title[2].cb.setCurrentText(item.attributes['level'].value)
                self.table1.setCellWidget(0, 1, self.main_title[0])
                self.table1.setCellWidget(0, 0, self.main_title[1])
                self.table1.setCellWidget(0, 2, self.main_title[2])

            itemlist = dom.getElementsByTagName('Others')
            self.rows.clear()

            for index, item in enumerate(itemlist):
                self.table.setRowCount(index + 1)  # и одну строку в таблице
                self.rows.append([widj_tab1.line_btn(1, 1, self), widj_tab1.line_btn(1, 2, self), widj_tab1.qbox_line(),
                                  widj_tab1.check_box(self, index)])
                self.table.setRowHeight(index, 50)
                self.rows[-1][0].line_text.setText(item.attributes['evklass'].value)
                self.rows[-1][1].line_text.setText(item.attributes['kadr'].value)
                self.rows[-1][2].cb.setCurrentText(item.attributes['level'].value)

                self.table.setCellWidget(index, 1, self.rows[-1][0])
                self.table.setCellWidget(index, 0, self.rows[-1][1])
                self.table.setCellWidget(index, 2, self.rows[-1][2])
