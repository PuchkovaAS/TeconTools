from collections import deque, namedtuple

import firebirdsql
from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from PyQt5.QtCore import pyqtSignal, QMimeData, QByteArray, QDataStream, QIODevice
from PyQt5.QtGui import QDoubleValidator, QIntValidator, QKeySequence, QPainter, QDrag
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QPushButton, QHBoxLayout
import main
from LybPyQT5.widgets.table import TableWidgetCustom

klassificator = namedtuple('klassificator', 'id name pid')
row_data = namedtuple('row_data', 'kadr evklass main')




def button_setting(name, function):
    button = QPushButton(name)
    button.setFixedHeight(30)
    button.clicked.connect(function)
    return button


def lineWap(name):
    label = QTableWidgetItem(name)
    # label.setWordWrap(True)
    label.setFlags(QtCore.Qt.ItemIsEditable)
    return label


def table_setting(name):
    table = TableWidgetCustom()  # Создаём таблицу
    table.setColumnCount(len(name))  # Устанавливаем три колонки
    table.setRowCount(0)  # и одну строку в таблице
    table.setHorizontalHeaderLabels(name)
    header = table.horizontalHeader()
    for index in range(len(name)):
        header.setSectionResizeMode(index, QHeaderView.Stretch)  # Stretch)

    # table.setSelectionBehavior(QAbstractItemView.SelectRows)  # Выделяет всю строку
    table.setWordWrap(True)

    # table.setSelectionBehavior(QAbstractItemView.SelectRows)  # Выделяет всю строку
    return table


def table_setting_drag(name):
    table = TableWidgetCustomDrag()  # Создаём таблицу
    table.setColumnCount(len(name))  # Устанавливаем три колонки
    table.setRowCount(0)  # и одну строку в таблице
    table.setHorizontalHeaderLabels(name)
    header = table.horizontalHeader()
    for index in range(len(name)):
        header.setSectionResizeMode(index, QHeaderView.Stretch)  # Stretch)

    # table.setSelectionBehavior(QAbstractItemView.SelectRows)  # Выделяет всю строку
    table.setWordWrap(True)

    # table.setSelectionBehavior(QAbstractItemView.SelectRows)  # Выделяет всю строку
    return table


def table_setting_drop(name):
    table = TableWidgetCustomDrop()  # Создаём таблицу
    table.setColumnCount(len(name))  # Устанавливаем три колонки
    table.setRowCount(0)  # и одну строку в таблице
    table.setHorizontalHeaderLabels(name)
    header = table.horizontalHeader()
    for index in range(len(name)):
        header.setSectionResizeMode(index, QHeaderView.Stretch)  # Stretch)

    # table.setSelectionBehavior(QAbstractItemView.SelectRows)  # Выделяет всю строку
    table.setWordWrap(True)

    # table.setSelectionBehavior(QAbstractItemView.SelectRows)  # Выделяет всю строку
    return table


class check_box(QWidget):
    def __init__(self, mainwindow, row):
        super().__init__()
        layout = QHBoxLayout()
        self.mainwindow = mainwindow
        self.row = row
        self.setLayout(layout)
        self.cb = QCheckBox('', self)
        self.cb.stateChanged.connect(self.state_changed)
        layout.addWidget(self.cb)

    def state_changed(self):
        pass


class check_box_line(QWidget):
    def __init__(self, line):
        super().__init__()
        layout = QHBoxLayout()
        line_text = QLabel(line)
        self.setLayout(layout)
        self.cb = QCheckBox('', self)
        layout.addWidget(self.cb)
        layout.addWidget(line_text)


class line_botton_switch(QWidget):
    def __init__(self, line, btn):
        super().__init__()
        layout = QHBoxLayout()
        line_text = QLabel(line)
        self.setLayout(layout)
        self.btn = QPushButton(btn)
        layout.addWidget(line_text)
        layout.addWidget(self.btn)


class line_btn(QWidget):
    my_signal = pyqtSignal()

    def __init__(self, grop, kadr, mainwin):
        super().__init__()
        self.mainwin = mainwin
        layout: QGridLayout = QGridLayout()
        self.btn = QPushButton("...")
        self.btn_open = QPushButton("open")
        self.btn_open.setMaximumWidth(50)
        self.line_text = QLineEdit(self)
        self.line_text.setText('')
        self.line_server = QLineEdit(self)
        self.line_server.setText('127.0.0.1')
        self.kadr = kadr
        if grop == 1:
            self.btn.clicked.connect(self.buttonClicked)
            self.btn_open.hide()
            self.line_server.hide()
        else:
            self.btn.clicked.connect(self.openBD)
            # self.line_text.setWordWrap(True)

        self.btn_open.clicked.connect(self.open_database)

        self.btn.setFixedSize(30, 30)

        self.line_text.setText('')
        self.line_text.setMinimumWidth(150)
        layout.addWidget(self.line_text, 0, 0, 1, 3)
        layout.addWidget(self.btn, 0, 3, 1, 1)
        layout.addWidget(self.line_server, 1, 0, 1, 3)
        layout.addWidget(self.btn_open, 1, 3, 1, 1)
        self.setLayout(layout)

    def buttonClicked(self):
        try:
            self.new = search_window(self, self.kadr)
            self.new.show()
        except Exception as e:
            QMessageBox().warning(self, "Ошибка", str(e.__str__()) + '\n Ошибка подлючения к базе', QMessageBox.Ok,
                                  QMessageBox.Ok)

    def open_database(self):
        self.mainwin.con = None
        try:
            self.mainwin.con = firebirdsql.connect(
                host=self.line_server.text(),
                database=self.line_text.text(),
                port=3050,
                user='sysdba',
                password='masterkey',
                charset='utf8'
            )

            self.line_text.setText(self.BD)
            self.cur = self.mainwin.con.cursor()
            self.get_klass(1)
            self.get_klass(2)
            self.mainwin.show_all()
            self.my_signal.emit()
        except Exception as e:
            self.mainwin.hide_all()
            QMessageBox().warning(self, "Ошибка", str(e.__str__()) + '\n Ошибка подлючения к базе', QMessageBox.Ok,
                                  QMessageBox.Ok)

    def openBD(self):
        self.mainwin.con = None
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        path, _ = QFileDialog.getOpenFileName(self, 'Открыть Базу', "", "GDB (*.GDB)", options=options)
        self.BD = path

        if path == '':
            return
        self.line_text.setText(self.BD)

    def get_klass(self, kadr):
        data = []
        list_klass = self.BD_serch(0, kadr)
        index_pos = 1
        while len(list_klass) != 0:
            list_klass_new = []
            for klass in list_klass:
                list_new = self.BD_serch(klass.id, kadr)
                data.append(
                    {'level': index_pos - 1, 'dbID': klass.id, 'parent_ID': klass.pid, 'short_name': klass.name,
                     'long_name': '',
                     'order': index_pos,
                     'pos': index_pos - 1})
                if len(list_new) != 0:
                    list_klass_new.extend(list_new)
            list_klass = list_klass_new
            index_pos += 1

        if kadr == 1:
            self.mainwin.evklass = data
        else:
            self.mainwin.kadrlist = data

    def BD_serch(self, PID, kadr):
        if kadr == 1:
            return self.get_evklassiv(PID)
        else:
            return self.get_GRPAGES(PID)

    def get_klassiv(self, PID):

        select = f"select ID, NAME from KLASSIFIKATOR WHERE PID = {PID}  and section = 2 order by name"
        self.cur.execute(select)
        return [klassificator(id, name, PID) for id, name in self.cur]

    def get_evklassiv(self, PID):

        select = f"select ID, NAME from EVKLASSIFIKATOR WHERE PID = {PID} order by name"
        self.cur.execute(select)
        return [klassificator(id, name, PID) for id, name in self.cur]

    def get_GRPAGES(self, PID):

        select = f"select ID, NAME from GRPAGES WHERE PID = {PID} order by name"
        self.cur.execute(select)
        return [klassificator(id, name, PID) for id, name in self.cur]


class line_btn_simple(QWidget):
    my_signal = pyqtSignal()

    def __init__(self, mainwin):
        super().__init__()
        self.mainwin = mainwin
        layout: QGridLayout = QGridLayout()
        self.btn = QPushButton("...")
        self.btn_open = QPushButton("open")
        self.btn_open.setMaximumWidth(50)
        self.line_text = QLineEdit(self)
        self.line_text.setText('')
        self.line_server = QLineEdit(self)
        self.line_server.setText('127.0.0.1')

        self.btn.clicked.connect(self.openBD)
        self.btn_open.clicked.connect(self.open_database)

        self.btn.setFixedSize(30, 30)

        self.line_text.setText('')
        self.line_text.setMinimumWidth(150)
        layout.addWidget(self.line_text, 0, 0, 1, 3)
        layout.addWidget(self.btn, 0, 3, 1, 1)
        layout.addWidget(self.line_server, 1, 0, 1, 3)
        layout.addWidget(self.btn_open, 1, 3, 1, 1)
        self.setLayout(layout)

    def open_database(self):
        self.mainwin.con = None
        try:
            self.mainwin.con = firebirdsql.connect(
                host=self.line_server.text(),
                database=self.line_text.text(),
                port=3050,
                user='sysdba',
                password='masterkey',
                charset='utf8'
            )

            self.cur = self.mainwin.con.cursor()
            self.my_signal.emit()
        except Exception as e:
            QMessageBox().warning(self, "Ошибка", str(e.__str__()) + '\n Ошибка подлючения к базе', QMessageBox.Ok,
                                  QMessageBox.Ok)

    def openBD(self):

        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        path, _ = QFileDialog.getOpenFileName(self, 'Открыть Базу', "", "GDB (*.GDB)", options=options)
        self.BD = path

        if path == '':
            return
        self.line_text.setText(self.BD)


class line_btn_path(QWidget):
    my_signal = pyqtSignal('PyQt_PyObject','PyQt_PyObject')

    def __init__(self, mainwin):
        super().__init__()
        self.mainwin = mainwin
        layout: QGridLayout = QGridLayout()
        self.btn = QPushButton("...")
        self.btn_open = QPushButton("open")
        self.btn_open.setMaximumWidth(50)
        self.line_text = QLineEdit(self)
        self.line_text.setText('')
        self.line_server = QLineEdit(self)
        self.line_server.setText('127.0.0.1')

        self.btn.clicked.connect(self.openBD)
        self.btn_open.clicked.connect(self.open_database)

        self.btn.setFixedSize(30, 30)

        self.line_text.setText('')
        self.line_text.setMinimumWidth(150)
        layout.addWidget(self.line_text, 0, 0, 1, 3)
        layout.addWidget(self.btn, 0, 3, 1, 1)
        layout.addWidget(self.line_server, 1, 0, 1, 3)
        layout.addWidget(self.btn_open, 1, 3, 1, 1)
        self.setLayout(layout)

    def open_database(self):
        self.mainwin.con = None
        try:
            con = firebirdsql.connect(
                host=self.line_server.text(),
                database=self.line_text.text(),
                port=3050,
                user='sysdba',
                password='masterkey',
                charset='utf8'
            )

            self.my_signal.emit(self.line_text.text(), self.line_server.text())
        except Exception as e:
            QMessageBox().warning(self, "Ошибка", str(e.__str__()) + '\n Ошибка подлючения к базе', QMessageBox.Ok,
                                  QMessageBox.Ok)

    def openBD(self):

        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        path, _ = QFileDialog.getOpenFileName(self, 'Открыть Базу', "", "GDB (*.GDB)", options=options)
        self.BD = path

        if path == '':
            return
        self.line_text.setText(self.BD)


class qbox_line(QWidget):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout()
        self.cb = QComboBox()

        # self.cb.setMaximumWidth(40)
        # self.cb.setMinimumHeight(25)
        self.cb.addItems(["0", "1", "2", "3", "4", "5"])
        # self.cb.currentIndexChanged.connect(self.selectionchange)
        layout.addWidget(self.cb)
        self.setLayout(layout)


class search_window(QWidget):
    def __init__(self, mainwindow, kadr):
        super().__init__()
        self.setStyleSheet(main_widjet.style)
        self.mainwindow = mainwindow
        self.kadr = kadr
        self.init_UI()

    def init_UI(self):

        self.tree = QtWidgets.QTreeView(self)
        layout: QHBoxLayout = QVBoxLayout()
        layout.addWidget(self.tree)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.tree)
        self.model = QtGui.QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['Классификатор'])
        self.tree.header().setDefaultSectionSize(180)
        self.tree.setModel(self.model)
        if self.kadr == 1:
            self.importData(self.mainwindow.mainwin.evklass)
        else:
            self.importData(self.mainwindow.mainwin.kadrlist)
        # self.tree.expandAll()

        self.setLayout(layout)

        self.tree.selectionModel().selectionChanged.connect(self.onSelectionChanged)
        self.btn = QPushButton("Принять")
        self.btn.clicked.connect(self.buttonClicked)
        # self.btn.setFixedSize(80, 30)
        layout.addWidget(self.btn)
        self.val = ''
        self.tree.collapseAll()
        self.setLayout(layout)

        self.setMinimumHeight(500)
        self.setMinimumWidth(600)

    def buttonClicked(self):
        self.mainwindow.line_text.setText(self.val)
        self.close()

    def onSelectionChanged(self, *args):
        for sel in self.tree.selectedIndexes():
            self.val = "/" + sel.data()
            while sel.parent().isValid():
                sel = sel.parent()
                self.val = "/" + sel.data() + self.val

    def importData(self, data, root=None):
        self.model.setRowCount(0)
        if root is None:
            root = self.model.invisibleRootItem()
        seen = {}
        values = deque(data)
        while values:
            value = values.popleft()
            if value['level'] == 0:
                parent = root
            else:
                pid = value['parent_ID']
                if pid not in seen:
                    values.append(value)
                    continue
                parent = seen[pid]
            dbid = value['dbID']
            parent.appendRow([
                QtGui.QStandardItem(value['short_name']),

            ])
            seen[dbid] = parent.child(parent.rowCount() - 1)


class lile_label(QWidget):
    def __init__(self, legent, number):
        super().__init__()
        main_layout = QHBoxLayout()
        self.line_edit = QLineEdit(number)
        validator = QIntValidator()
        self.line_edit.setValidator(validator)
        self.line_edit.setMaximumHeight(30)
        main_layout.addWidget(QLabel(legent))
        main_layout.addWidget(self.line_edit)

        self.setLayout(main_layout)


class lile_label_name(QWidget):
    def __init__(self, legent, number):
        super().__init__()
        main_layout = QHBoxLayout()
        self.line_edit = QLineEdit(number)
        self.line_edit.setMaximumHeight(30)
        main_layout.addWidget(QLabel(legent))
        main_layout.addWidget(self.line_edit)

        self.setLayout(main_layout)


class lile_label(QWidget):
    def __init__(self, legent, number):
        super().__init__()
        main_layout = QHBoxLayout()
        self.line_edit = QLineEdit(number)
        validator = QIntValidator()
        self.line_edit.setValidator(validator)
        self.line_edit.setMaximumHeight(35)
        main_layout.addWidget(QLabel(legent))
        main_layout.addWidget(self.line_edit)

        self.setLayout(main_layout)
