import sqlite3
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
from PyQt5.QtCore import QSortFilterProxyModel, QThread, pyqtSignal
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from PyQt5.QtWidgets import QTableWidgetItem, QHBoxLayout, QProgressBar, QFileDialog, \
    QMessageBox, QSplitter
from openpyxl import load_workbook

import scripts.analyzer as analyzer
from LybPyQT5.widgets.button import SimpleBtn
from LybPyQT5.widgets.db_path import SimpleDBPath
from LybPyQT5.widgets.line_text import LineText
from LybPyQT5.widgets.tab import LibTab
from LybPyQT5.widgets.table import TableView, TableWidget



class AnalyzerThread(QThread):
    signal = pyqtSignal('PyQt_PyObject')
    error = pyqtSignal('PyQt_PyObject')

    def __init__(self, path_fbd, server, path_result):
        QThread.__init__(self)
        self.path_fbd = path_fbd
        self.server = server
        self.path_result = path_result

    # run method gets called when we start the thread
    def run(self):
        # self.error.emit(f"Упс, ошибочка вышла :(, ")
        try:
            new_BD = analyzer.DB_Result(path_result=self.path_result, path_fbd=self.path_fbd, server=self.server)
            new_BD.firebird_db_init()
            self.signal.emit(self.path_result)
        except Exception as err:
            self.error.emit(f"Упс, ошибочка вышла :(, \n {err.__str__()}")


class SaveExcelThread(QThread):
    signal = pyqtSignal()
    error = pyqtSignal('PyQt_PyObject')

    def __init__(self, path_db, path_excel, proxy):
        QThread.__init__(self)
        self.path_sql_lite = path_db
        self.proxy = proxy
        self.path_excel = path_excel

    # run method gets called when we start the thread
    def run(self):
        try:
            wb = load_workbook('templates/to_excel/template.xlsx')
            ws = wb['Sheet1']
            conn = sqlite3.connect(self.path_sql_lite)
            """ Создание БД в памяти """
            # self.conn = sqlite3.connect(':memory:')
            cursor = conn.cursor()

            for row in range(self.proxy.rowCount()):
                id_marka = self.proxy.data(self.proxy.index(row, 1))
                cursor.execute(
                    f"select MARKA, KLASS, TYPE, PLC_NAME, NAME, DISC, OBJSIGN, OBJNUMBER, PLC_VARNAME, ARH_PER, KKS, OBJDPARAM, SREZCONTROL, EVGROUP, PLC_ADRESS, PLC_GR, TEMPLATE from ResultTable, AdditionalTable where ResultTable.id_marka = {id_marka} and ResultTable.id_marka = AdditionalTable.id_marka")
                MARKA, KLASS, TYPE, PLC_NAME, NAME, DISC, OBJSIGN, OBJNUMBER, PLC_VARNAME, ARH_PER, KKS, OBJDPARAM, SREZCONTROL, EVGROUP, PLC_ADRESS, PLC_GR, TEMPLATE = \
                    cursor.fetchall()[0]

                KLASS = KLASS.replace('//', '\\')
                EVGROUP = EVGROUP.replace('//', '\\')
                ws.append(
                    ['', '', 'TEHOBJ', MARKA, TYPE, NAME, DISC, OBJSIGN, OBJNUMBER, PLC_VARNAME, ARH_PER, KKS,
                     OBJDPARAM,
                     SREZCONTROL, KLASS, EVGROUP, PLC_NAME, PLC_ADRESS, PLC_GR, TEMPLATE])

            conn.close()
            wb.save(self.path_excel)
            self.signal.emit()
        except Exception as err:
            self.error.emit("Ошибка", f"Упс, ошибочка вышла :(, \n {err.__str__()}")


class MySortFilterProxyModel(QSortFilterProxyModel):
    def __init__(self, parent=None):
        super(MySortFilterProxyModel, self).__init__(parent)
        self.filters = {}

    def setFilterByColumn(self, regex, column):
        self.filters[column] = regex
        self.invalidateFilter()

    def filterAcceptsRow(self, sourceRow, sourceParent):

        for key, regex in self.filters.items():
            # regex.setPatternSyntax(QRegExp.RegExp)
            ix = self.sourceModel().index(sourceRow, key, sourceParent)
            if ix.isValid():
                text = str(self.sourceModel().data(ix))

                # return regex.exactMatch(text)
                if not regex.indexIn(text) >= 0:
                    return False
        return True


class Tab(LibTab):
    def __init__(self):
        super(Tab, self).__init__()

        self.view = TableView(click_func=self.view_table_info)

        self.table_info = TableWidget(columns=2)

        hbox_firbird = QHBoxLayout()
        self.progressbar = QProgressBar(textVisible=True)

        self.bd_window = SimpleDBPath(mainwin=self)
        self.bd_window.my_signal.connect(self.BD_is_open)
        hbox_firbird.addWidget(self.bd_window)

        btn_start_analyze = SimpleBtn(label=f"Analyze", click_func=self.open_firebird)

        hbox_firbird.addWidget(btn_start_analyze)

        btn_export = SimpleBtn(label=f"To excel", click_func=self.to_excel)

        hbox_firbird.addWidget(btn_export)

        hbox_firbird.addWidget(self.progressbar)
        # hbox_firbird.addSpacing(1)

        open_sql_lite = SimpleBtn(label=f"Open existing", click_func=self.open_lite)

        hbox_firbird.addWidget(open_sql_lite)
        hbox_firbird.minimumSize()

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.view)
        splitter.addWidget(self.table_info)

        self.main_layout.addLayout(hbox_firbird, 0, 0, 1, 1)
        self.main_layout.addWidget(splitter, 2, 0, 1, 1)


    def BD_is_open(self, path, server):
        self.path_fbd = path
        self.server = server
        self.progressbar.setMaximum(100)
        self.progressbar.setMinimum(0)
        self.progressbar.setValue(100)

    def to_excel(self):
        try:
            options = QFileDialog.Options()
            # options |= QFileDialog.DontUseNativeDialog
            path, _ = QFileDialog.getSaveFileName(self, 'Сохранить файл импорта', "", "xls (*.xls)", options=options)

            if path == '':
                return

            if path.find('.xls') == -1:
                path += '.xls'

            self.save_excel = SaveExcelThread(path_db=self.path_sql_lite, proxy=self.proxy, path_excel=path)
            self.save_excel.signal.connect(self.excel_succes)
            self.save_excel.error.connect(self.errorMess)
            self.progressbar.setMaximum(0)
            self.progressbar.setMinimum(0)
            self.save_excel.start()

        except Exception as err:
            QMessageBox.warning(self, "Ошибка", f"Упс, ошибочка вышла :(, \n {err.__str__()}", QMessageBox.Ok,
                                QMessageBox.Ok)

    def excel_succes(self):
        self.progressbar.setMaximum(100)
        self.progressbar.setMinimum(0)
        self.progressbar.setValue(100)
        QMessageBox().information(self, "Экспорт в excel", 'Экспорт прошел успешно', QMessageBox.Ok)

    def open_firebird(self):
        try:
            options = QFileDialog.Options()
            # options |= QFileDialog.DontUseNativeDialog
            path, _ = QFileDialog.getSaveFileName(self, 'Сохранить sql_lite', "", "db (*.db)", options=options)

            if path == '':
                return

            if path.find('.db') == -1:
                path += '.db'

            self.thread_bd = AnalyzerThread(path_result=path, path_fbd=self.path_fbd,
                                            server=self.server)  # This is the thread object

            self.thread_bd.signal.connect(self.thread_finished)
            self.thread_bd.error.connect(self.errorMess)
            self.progressbar.setMaximum(0)
            self.progressbar.setMinimum(0)
            self.thread_bd.start()
        except Exception as err:
            QMessageBox.warning(self, "Ошибка", f"Упс, ошибочка вышла :(, \n {err.__str__()}", QMessageBox.Ok,
                                QMessageBox.Ok)

    def errorMess(self, message):
        self.progressbar.setMaximum(100)
        self.progressbar.setMinimum(0)
        self.progressbar.setValue(0)
        QMessageBox().warning(self, "Ошибка", str(message), QMessageBox.Ok,
                              QMessageBox.Ok)

    def thread_finished(self, path):
        self.progressbar.setMaximum(100)
        self.progressbar.setMinimum(0)
        self.progressbar.setValue(100)
        self.initializedModel(path)

    def open_lite(self):
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        path, _ = QFileDialog.getOpenFileName(self, 'Открыть sql_lite', "", "db (*.db)", options=options)

        if path == '':
            return

        with open(path, "r", encoding='UTF-8') as f:
            self.initializedModel(path)

    def initializedModel(self, path):
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName(path)
        self.db.open()
        self.path_sql_lite = path

        self.model = QSqlTableModel()
        self.model.setTable("ResultTable")
        self.model.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.model.select()

        while self.model.canFetchMore():
            self.model.fetchMore()
        self.view.resizeColumnsToContents()

        self.proxy = MySortFilterProxyModel(self)
        self.proxy.setSourceModel(self.model)

        self.view.setModel(self.proxy)

        self.dict_column = {self.model.record().fieldName(x): x for x in range(self.model.columnCount())}

        hbox_search = QHBoxLayout()
        for placeholder in [self.model.record().fieldName(x) for x in range(self.model.columnCount())]:
            hbox_search.addWidget(LineText(placeholder=placeholder, func_text_change=self.on_lineEdit_textChanged))

        self.table_info.setRowCount(len(self.dict_column.keys()))
        for index, property_table in enumerate(self.dict_column.keys()):
            self.table_info.setItem(index, 0, QTableWidgetItem(property_table))

        self.main_layout.addLayout(hbox_search, 1, 0, 1, 1)

    def view_table_info(self, signal):
        current_row = signal.row()
        for index in range(len(self.dict_column.keys())):
            table_index = self.proxy.index(current_row, index)
            self.table_info.setItem(index, 1, QTableWidgetItem(str(self.proxy.data(table_index))))
        self.table_info.resizeRowsToContents()

    @QtCore.pyqtSlot(str)
    def on_lineEdit_textChanged(self, text):
        search = QtCore.QRegExp(text,
                                QtCore.Qt.CaseInsensitive,
                                QtCore.QRegExp.RegExp
                                )

        self.proxy.setFilterByColumn(search, self.dict_column[self.sender().placeholderText()])

#
# if __name__ == "__main__":
#     import sys
#
#     app = QApplication(sys.argv)
#     main = myWindow()
#     main.show()
#     main.resize(400, 600)
#     sys.exit(app.exec_())
