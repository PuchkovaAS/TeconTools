import copy
import sqlite3
from collections import defaultdict
from dataclasses import dataclass

import firebirdsql
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from jinja2 import Environment, FileSystemLoader, BaseLoader

import scripts.get_templates_to_db as get_templates_to_db
from LybPyQT5.widgets.button import SimpleBtn
from LybPyQT5.widgets.db_path import SimpleDBPath
from LybPyQT5.widgets.group_box import GroupBox
from LybPyQT5.widgets.label import InfoLabel, style_warning
from LybPyQT5.widgets.search_window import SearchWindow
from LybPyQT5.widgets.spin_box import SpinBox
from LybPyQT5.widgets.tab import LibTab
from LybPyQT5.widgets.text_editor import TextEditor
from LybPyQT5.widgets.tree import SimpleTree
from main import resource_path

btn_main = 30
btn_other = 25
anim_main = 7
anim_other = 4

temp_db_path = './resources/test.db'


class WindowAddTemplate(QWidget):

    def __init__(self, mainwindow):
        super().__init__()
        self.mainwindow = mainwindow
        self.setWindowTitle('Шаблоны')
        self.setWindowIcon(QIcon(resource_path('resources/main_ico.png')))
        layout = QGridLayout()
        self.setLayout(layout)

        self.desc_text = TextEditor(placeholder='Описание')
        self.name_text = TextEditor(placeholder='Уникальное имя')

        self.path_file = QtWidgets.QLabel('Файл шаблон')

        btn_open = SimpleBtn(label='...', click_func=self.get_path, height=30, width=30)
        btn_except = SimpleBtn(label='Добавить', click_func=self.add_to_bd)


        layout.addWidget(self.name_text, 0, 0, 1, 3)
        layout.addWidget(self.path_file, 1, 0, 1, 2)
        layout.addWidget(btn_open, 1, 2, 1, 1)
        layout.addWidget(self.desc_text, 2, 0, 10, 3)
        layout.addWidget(btn_except, 12, 0, 1, 3)

        self.setLayout(layout)

        self.setMinimumHeight(500)
        self.setMinimumWidth(600)

    def get_path(self):
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        path, _ = QFileDialog.getOpenFileName(self, 'Открыть xml', "", "Xml (*.xml)", options=options)

        if path == '':
            return

        self.path_file.setText(path)

    def add_to_bd(self):
        try:
            if self.path_file.text() == '':
                raise Exception
            self.xml_analize = get_templates_to_db.XmlAnalize()

            self.xml_analize.signal.connect(self.thread_finished)
            self.xml_analize.error.connect(self.errorMess)
            self.xml_analize.start_work(path=self.path_file.text(),
                                        name=self.name_text.text(),
                                        desc=self.desc_text.toPlainText())
        except Exception as err:
            QMessageBox().warning(self, "Ошибка", str(err.__str__()), QMessageBox.Ok,
                                  QMessageBox.Ok)

    def errorMess(self, err):
        QMessageBox().warning(self, "Ошибка", str(err.__str__()), QMessageBox.Ok,
                              QMessageBox.Ok)
        self.close()

    def thread_finished(self):
        QMessageBox().information(self, 'Готово', 'Шаблон добавлен в базу', QMessageBox.Ok)
        self.mainwindow.get_list_templ()
        self.close()

@dataclass
class Page:
    ID: int = 0
    PID: int = 0
    NAME: str = ''


class PagesStruct:

    def __init__(self, cursor):
        self.pages_dict_SQL = {}
        self.pages_dict_primarily = {}
        self.parent_dict = defaultdict(list)
        self.pages_dict_name = defaultdict(list)
        self.cursor = cursor
        self.get_all_pages()
        self.get_struct_tree()
        self.get_struct_pages()

    def get_all_pages(self):
        self.cursor.execute(f"""select ID, PID, NAME from GRPAGES""")
        self.pages_dict_primarily = {ID: Page(ID=ID, PID=PID, NAME=NAME) for ID, PID, NAME in self.cursor.fetchall()}
        self.pages_dict_SQL = copy.deepcopy(self.pages_dict_primarily)

    def get_struct_tree(self):
        for page in self.pages_dict_SQL.values():
            self.parent_dict[page.PID].append(page.ID)

    def get_struct_pages(self):
        for page in self.pages_dict_SQL.values():
            while True:
                try:
                    parent = self.pages_dict_SQL[page.PID]
                    page.PID = parent.PID
                    page.NAME = f"{parent.NAME}//{page.NAME}"
                except:
                    break

        for page in self.pages_dict_SQL.values():
            self.pages_dict_name[page.NAME].append(page.ID)


class EvklassStruct(PagesStruct):
    def get_all_pages(self):
        self.cursor.execute(f"""select ID, PID, NAME from EVKLASSIFIKATOR""")
        self.pages_dict_primarily = {ID: Page(ID=ID, PID=PID, NAME=NAME) for ID, PID, NAME in self.cursor.fetchall()}
        self.pages_dict_SQL = copy.deepcopy(self.pages_dict_primarily)


class PagesView(QWidget):
    button_clicked = pyqtSignal()

    def __init__(self, Page='Не найден'):
        super().__init__()
        layout = QGridLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(0, 0, 0, 0)
        # label = QtWidgets.QLabel('Группа событий:')
        # hlay = QHBoxLayout()
        # button = QtWidgets.QPushButton('...')
        #
        # button.setFixedWidth(30)
        # button.setFixedHeight(30)
        # button.clicked.connect(self.open_view_page)
        # hlay.addWidget(label)

        # hlay.addWidget(button)
        self.label = InfoLabel(Page)
        if Page == 'Не найден':
            self.label.setStyleSheet(style_warning)

        self.label.doubleClicked.connect(self.open_view_page)
        layout.addWidget(self.label, 0, 0)
        # layout.addWidget(button, 0, 2)
        layout.setContentsMargins(3, 3, 3, 3)
        layout.setSpacing(5)
        # layout.setColumnStretch(1, 1)
        # layout.setColumnStretch(3, 2)
        # layout.setAlignment(Qt.AlignTop)
        self.setLayout(layout)

    def open_view_page(self):
        self.button_clicked.emit()

    def state_changed(self):
        pass


class Tab(LibTab):
    def __init__(self):
        super().__init__()
        self.initData()
        self.initUI()

    def initData(self):
        self.init_template()

    def temp_db_open(self, temp_db_path):
        try:
            self.temp_conn = sqlite3.connect(temp_db_path)
            self.temp_cursor = self.temp_conn.cursor()
            self.get_list_templ()
        except Exception as err:
            QMessageBox().warning(self, "Ошибка", str(err.__str__()), QMessageBox.Ok,
                                  QMessageBox.Ok)

    def get_list_templ(self):
        self.temp_cursor.execute("""SELECT NAME, desc FROM Templates""")
        # self.temp_cursor.execute("""select * from sqlite_master where name='Templates' and type='table';""")
        self.add_templates_from_db(self.temp_cursor.fetchall())


    def initUI(self):


        layout_gr = QHBoxLayout()
        self.level_able = SpinBox(max=5, min=1, value=2)
        layout_gr.addWidget(self.level_able)

        self.tree = SimpleTree(header=['Группа событий', 'Кадр'], count_column=2, click_func=self.check_status)

        self.bd_window = SimpleDBPath(mainwin=self)
        self.bd_window.my_signal.connect(self.BD_is_open)

        move_up_btn = SimpleBtn(label='UP', click_func=lambda: self.move_row(direction=-1))
        move_down_btn = SimpleBtn(label='DOWN', click_func=lambda: self.move_row(direction=1))

        layout_btn = QVBoxLayout()
        layout_btn.addWidget(move_up_btn)
        layout_btn.addWidget(move_down_btn)


        self.width_level = SpinBox(max=50, value=10, min=0)
        self.width_page = SpinBox(max=3000, value=1920, min=0)
        self.width_btn = SpinBox(max=3000, value=274, min=0)
        self.width_all_child = SpinBox(max=1000, value=0, min=0)

        self.prefix_page = QLineEdit('Меню_')
        self.find_page = QLineEdit('')

        self.combo_template = QComboBox(self)
        self.combo_template.activated[str].connect(self.comboChange)

        self.temp_db_open(temp_db_path=temp_db_path)

        self.count_obj = SpinBox(max=50, min=0, value=0, change_func=self.change_btn_width)

        layout_page = QGridLayout()
        layout_page.addWidget(QLabel('Приставка\nкадра'), 0, 0, 1, 1)
        layout_page.addWidget(QLabel('Поиск\nкадра'), 1, 0, 1, 1)

        layout_page.addWidget(QLabel('Ширина кадра'), 2, 0, 1, 1)
        layout_page.addWidget(QLabel('Ширина кнопки'), 3, 0, 1, 1)

        layout_page.addWidget(QLabel('Отступ\nдля дочерних'), 4, 0, 1, 1)
        layout_page.addWidget(QLabel('Отступ\nиерархии'), 5, 0, 1, 1)

        layout_page.addWidget(QLabel('Кол-во в ряду'), 6, 0, 1, 1)

        layout_page.addWidget(self.prefix_page, 0, 1, 1, 1)
        layout_page.addWidget(self.find_page, 1, 1, 1, 1)

        layout_page.addWidget(self.width_page, 2, 1, 1, 1)
        layout_page.addWidget(self.width_btn, 3, 1, 1, 1)

        layout_page.addWidget(self.width_all_child, 4, 1, 1, 1)
        layout_page.addWidget(self.width_level, 5, 1, 1, 1)

        layout_page.addWidget(self.count_obj, 6, 1, 1, 1)

        self.check_up_down = QCheckBox('\tВверх(0)\n\tВниз(1)')

        layout_generation = QHBoxLayout()
        layout_generation.addWidget(self.check_up_down)
        self.btn_gen = SimpleBtn(label='Генерировать', click_func=self.gen_and_save)
        layout_generation.addWidget(self.btn_gen)

        btn_open_templ_editor = SimpleBtn(label='...', height=30, width=30, click_func=self.open_edit_templ)

        layout_template = QGridLayout()
        layout_template.addWidget(QLabel('Шаблон'), 0, 0, 1, 1)
        layout_template.addWidget(self.combo_template, 0, 1, 1, 3)
        layout_template.addWidget(QLabel('Редактировать'), 1, 0, 1, 3)
        layout_template.addWidget(btn_open_templ_editor, 1, 3, 1, 1)

        self.main_layout.addWidget(self.tree, 0, 0, 27, 1)
        self.main_layout.addWidget(self.bd_window, 0, 3, 1, 2)

        self.main_layout.setRowStretch(3, 3)
        self.main_layout.addWidget(GroupBox(name='Уровень иерархии', layout=layout_gr), 1, 4, 2, 1)
        self.main_layout.addWidget(GroupBox(name='Иерархия', layout=layout_btn), 1, 3, 2, 1)
        self.main_layout.addWidget(GroupBox(name='Настройка шаблонов', layout=layout_template), 3, 3, 2, 2)
        self.main_layout.addWidget(GroupBox(name='Настройка страницы', layout=layout_page), 6, 3, 2, 2)
        self.main_layout.addWidget(GroupBox(name='Генерация', layout=layout_generation), 8, 3, 2, 2)

        self.setLayout(self.main_layout)


    def open_edit_templ(self):
        self.new_win = WindowAddTemplate(mainwindow=self)
        self.new_win.show()

    def add_templates_from_db(self, temp_list):
        self.combo_template.clear()
        for index, name in enumerate(temp_list):
            self.combo_template.addItem(name[0])
            self.combo_template.setItemData(index, name[1], Qt.ToolTipRole)
        self.get_templ_from_db(templ_name=self.combo_template.currentText())

    def init_template(self):
        env = Environment(loader=FileSystemLoader('.'))
        self.template_Link = env.get_template('templates/tab1_1/page_link.html')
        self.template_Main = env.get_template('templates/tab1_1/main.html')
        self.template_Page = env.get_template('templates/tab1_1/page.html')

    def get_templ_from_db(self, templ_name):
        self.temp_cursor.execute(
            f"""SELECT ChildButton, ChildButton_dy, ChildParButton, ChildParButton_dy, ParentButton, ParentButton_dy, ColorStyle FROM Templates where name='{templ_name}'""")

        sql_data = self.temp_cursor.fetchall()[0]
        self.template_ChildButton = Environment(loader=BaseLoader).from_string(sql_data[0])
        self.dy_ChildButton = int(sql_data[1])
        self.template_ChildParButton = Environment(loader=BaseLoader).from_string(sql_data[2])
        self.dy_ChildParButton = int(sql_data[3])
        self.template_ParentButton = Environment(loader=BaseLoader).from_string(sql_data[4])
        self.dy_ParentButton = int(sql_data[5])
        self.template_ColorStyle = sql_data[6]

    def comboChange(self):
        self.get_templ_from_db(templ_name=self.combo_template.currentText())

    def check_status(self):
        count_row = 0
        for item in self.tree.findItems("", Qt.MatchContains | Qt.MatchRecursive):
            if item.checkState(0) != 0 and item.parent().parent() is None:
                count_row += 1
        self.count_obj.setValue(count_row)
        self.width_btn.setValue(self.width_page.value() // count_row if count_row > 0 else 274)

    def change_btn_width(self):
        self.width_btn.setValue(
            self.width_page.value() // self.count_obj.value() if self.count_obj.value() > 0 else 274)

    def BD_is_open(self, fbd_path, server):
        try:
            self.db_open(server, fbd_path)
            self.tree_completion()
        except Exception as err:
            QMessageBox().warning(self, "Ошибка", str(err.__str__()), QMessageBox.Ok,
                                  QMessageBox.Ok)

    def move_row(self, direction):
        try:
            item = self.tree.currentItem()
            widget = self.tree.itemWidget(item, 1)
            parent = item.parent()
            index = parent.indexOfChild(item)
            if (direction == -1 and index == 0) or (direction == 1 and index == parent.childCount() - 1):
                return
            child = parent.takeChild(index)
            parent.insertChild(index + direction, child)
            if widget:
                new_widget = PagesView(Page=widget.label.text())
                new_widget.button_clicked.connect(self.open_view_page)
                self.tree.setItemWidget(child, 1, new_widget)
            self.tree.setCurrentItem(child)

        except Exception as err:
            QMessageBox().warning(self, "Ошибка", str(err.__str__()), QMessageBox.Ok,
                                  QMessageBox.Ok)

    def get_all_path(self, item):
        val = "//" + item.data(0, 0)
        while item.parent() and item.parent().data(0, 0) != 'Все события':
            item = item.parent()
            val = "//" + item.data(0, 0) + val

        return val

    def add_ChildButton(self, name_grup, name_page, page_id, dx):
        self.contents_btn.append(str(
            self.template_ChildButton.render(WIDTH=self.width_btn.value() - dx, Y=self.y,
                                             NAME_GRUP=name_grup,
                                             LINK=name_page,
                                             PAGE_ID=page_id,
                                             X=dx)))
        self.y += self.dy_ChildButton

    def add_ChildParButton(self, name_grup, name_page, page_id, dx):
        self.contents_btn.append(str(
            self.template_ChildParButton.render(WIDTH=self.width_btn.value(), Y=self.y,
                                                NAME_GRUP=name_grup,
                                                LINK=name_page,
                                                PAGE_ID=page_id,
                                                X=dx)))
        self.y += self.dy_ChildParButton

    def add_ParentButton(self, name_grup, name_page, page_id):
        self.main_page_btn.append(str(
            self.template_ParentButton.render(WIDTH=self.width_btn.value(), Y=0,
                                              NAME_GRUP=name_grup,
                                              MENULINK=name_page,
                                              PAGE_ID=page_id,
                                              X=self.x_main)))
        self.x_main += self.width_btn.value()

    def add_page(self, full_name_page):
        self.contents_page.append(str(
            self.template_Page.render(NAME_PAGE=full_name_page,
                                      WIDTH=self.width_btn.value(),
                                      HEIGHT=self.y,
                                      layers=self.contents_btn)))

        if not self.check_up_down.isChecked():
            height = 0
            if self.count_menu >= self.count_obj.value():
                self.y_main += btn_main
                self.x_main = 0
                self.count_menu = 0

        self.link_page_btn.append(str(
            self.template_Link.render(FULL_PAGE_NAME=full_name_page, PAGE_ID=self.page_id)))

        self.page_id += 1
        self.count_menu += 1

        self.contents_btn = []
        self.y = 0

    def add_common_page(self, full_name_page):
        self.contents_page.append(str(
            self.template_Page.render(NAME_PAGE=full_name_page,
                                      WIDTH=self.width_page.value(),
                                      HEIGHT=self.dy_ParentButton,
                                      layers=self.main_page_btn)))

    def gen_and_save(self):
        try:
            self.contents_btn = []
            self.contents_page = []
            self.main_page_btn = []
            self.link_page_btn = []

            # connection = eval(self.text_panel.toPlainText())
            options = QFileDialog.Options()
            # options |= QFileDialog.DontUseNativeDialog
            fileName, _ = QFileDialog.getSaveFileName(self, "Сохранить xml", "", "xml (*.xml)", options=options)

            if fileName == '':
                return

            if fileName.find('.xml') == -1:
                fileName += '.xml'

            self.y = 0
            self.x_main = 0
            self.y_main = 0
            self.page_id = 1
            self.count_menu = 0

            with open(fileName, "w", encoding='utf8') as f:
                for item in self.tree.findItems("", Qt.MatchContains | Qt.MatchRecursive):
                    if item.checkState(0) != 0:
                        item_ident = self.tree.itemWidget(item, 1)
                        if item_ident is None:
                            if len(self.contents_btn) != 0:
                                if not self.check_up_down.isChecked():
                                    #     вверх
                                    self.add_ChildParButton(name_grup=self.save_name_grup,
                                                            name_page=f'{self.prefix_page.text()}{self.save_name_grup}',
                                                            page_id=None, dx=0)
                                self.add_page(full_name_page=f'{self.prefix_page.text()}{self.save_name_grup}')
                            # верхняя
                            self.save_name_grup = item.data(0, 0)
                            # if self.check_up_down.isChecked():

                            if self.check_up_down.isChecked():
                                # вниз
                                self.add_ChildParButton(name_grup=self.save_name_grup,
                                                        name_page=f'{self.prefix_page.text()}{self.save_name_grup}',
                                                        page_id=None, dx=0)
                            self.add_ParentButton(name_grup=self.save_name_grup,
                                                  name_page=f'{self.prefix_page.text()}{self.save_name_grup}',
                                                  page_id=self.page_id)

                        else:
                            name_page = self.tree.itemWidget(item, 1).label.text()
                            name_page_too = name_page.split('//')[-1]
                            level_page = self.find_level_page(item)
                            self.add_ChildButton(name_grup=item.data(0, 0), name_page=name_page_too,
                                                 page_id=self.pages.pages_dict_name[name_page][
                                                     0] if name_page != 'Не найден' else -1,
                                                 dx=level_page * self.width_level.value() + self.width_all_child.value())

                if len(self.contents_btn) != 0:
                    if not self.check_up_down.isChecked():
                        #     вверх
                        self.add_ChildParButton(name_grup=self.save_name_grup,
                                                name_page=f'{self.prefix_page.text()}{self.save_name_grup}',
                                                page_id=None, dx=0)

                self.add_page(full_name_page=f'{self.prefix_page.text()}{self.save_name_grup}')

                self.add_common_page(full_name_page='Нижний фрейм')
                f.write(self.template_Main.render(pages=self.contents_page, page_links=self.link_page_btn,
                                                  colorstyles=self.template_ColorStyle))
                QMessageBox().information(self, 'Готово', 'Файл экспорта создан', QMessageBox.Ok)
        except Exception as err:
            QMessageBox().warning(self, "Ошибка", str(err.__str__()), QMessageBox.Ok,
                                  QMessageBox.Ok)

    def find_level_page(self, item):
        level = 0

        while item.parent():
            level += 1
            item = item.parent()

        return level - 2 if level - 2 >= 0 else 0

    def db_open(self, server, path_fbd):
        self.fdb_conn = firebirdsql.connect(
            host=server,
            database=path_fbd,
            port=3050,
            user='sysdba',
            password='masterkey',
            charset='utf8'
        )
        self.fdb_cur = self.fdb_conn.cursor()

        # определение страниц кода и кадров

        self.pages = PagesStruct(self.fdb_cur)
        self.evklid = EvklassStruct(self.fdb_cur)

    def get_main_id(self, NAME='[Все технологические]', TABLE='EVKLASSIFIKATOR'):
        self.fdb_cur.execute(f"""select ID from {TABLE} where NAME = '{NAME}'""")
        return self.fdb_cur.fetchall()[0][0]

    def prefix_name_change(self, page_last):
        if self.find_page.text():
            list_of_name = page_last.split('//')
            new_list = list(map(lambda name: f'{self.find_page.text()}{name}', list_of_name))
            new_name = f'//'.join(new_list)
            return f"Root//{self.find_page.text()}//{new_name}"
        else:
            return f'Root//Кадры//{self.find_page.text()}{page_last}'


    def find_page_name(self, evk_id):
        first, page_last_name = self.evklid.pages_dict_SQL[evk_id].NAME.split('[Все технологические]//')
        id_page = self.pages.pages_dict_name.get(self.prefix_name_change(page_last_name), None)
        return self.pages.pages_dict_SQL[id_page[0]].NAME if id_page else 'Не найден'

    def add_tree(self, parent, id, level=0):
        for child_id in self.evklid.parent_dict[id]:
            evklass = self.evklid.pages_dict_primarily[child_id]
            child = QtWidgets.QTreeWidgetItem(parent)

            if level <= 0:
                child.setFlags(child.flags() | Qt.ItemIsUserCheckable | Qt.ItemIsAutoTristate)
            else:
                child.setFlags(child.flags() | Qt.ItemIsUserCheckable)
            # | Qt.ItemIsEditable | Qt.ItemIsSelectable | Qt.ItemIsTristate| Qt.ItemIsUserTristate
            child.setText(0, evklass.NAME)
            page_name = self.find_page_name(evk_id=child_id)

            row_data = PagesView(Page=page_name)
            row_data.button_clicked.connect(self.open_view_page)
            # child.setExpanded(True)
            if parent.text(0) != 'Все события':
                self.tree.setItemWidget(child, 1, row_data)
            child.setCheckState(0, Qt.Unchecked)
            if level + 1 < self.level_able.value():
                self.add_tree(parent=child, id=evklass.ID, level=level + 1)

    def tree_completion(self):
        self.tree.clear()
        item = QtWidgets.QTreeWidgetItem(self.tree)
        item.setText(0, 'Все события')
        main_id = self.get_main_id()
        self.add_tree(parent=item, id=main_id)
        self.tree.expandItem(item)

    def open_view_page(self):
        self.new_win = SearchWindow(pages=self.pages, current_row=self.sender(), prefix=self.find_page.text())
        self.new_win.show()
