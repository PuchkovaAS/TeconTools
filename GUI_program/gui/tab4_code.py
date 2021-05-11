# -*- coding: cp1251 -*-
import copy
import re
from collections import namedtuple

import firebirdsql
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import *

from LybPyQT5.widgets.button import SimpleBtn
from LybPyQT5.widgets.check_box import CheckBox
from LybPyQT5.widgets.db_path import SimpleDBPath
from LybPyQT5.widgets.line_text import LineText
from LybPyQT5.widgets.tab import LibTab
from LybPyQT5.widgets.text_editor import TextEditor

row_data = namedtuple('row_data', 'kadr evklass main')


class CloneThread(QThread):
    signal = pyqtSignal('PyQt_PyObject')

    def __init__(self, con=None, text=None, reverce_exv=False, plc_name='', plc_res='', setting=None):
        QThread.__init__(self)
        self.con = con
        self.text = text
        self.reverce_exv = reverce_exv
        self.plc_name = plc_name
        self.plc_res = plc_res
        self.sett_checkbox = setting

    # run method gets called when we start the thread
    def run(self):
        if not self.reverce_exv:
            result = self.generat()
        else:
            result = self.reverce_code()

        self.signal.emit(result)

    def find_tempalte(self, template, function_str, function_get, string_some, replace_teml='%s'):
        name_registers = re.findall(template, string_some)

        if len(name_registers) == 0:
            return string_some

        list_of_id = [function_get(name_register) for name_register in name_registers]
        new_code_line = copy.deepcopy(string_some)
        for name_register in name_registers:
            new_code_line = new_code_line.replace(replace_teml % name_register, '{}')

        new_code_line = new_code_line.format(*(list(map(function_str, list_of_id))))

        return new_code_line

    def get_card_from_com(self, slovo):
        if not self.sett_checkbox.isChecked():
            select = f"select NAME from ISACARDS WHERE MARKA = '{slovo}' and resid in (select id from RESOURCES where name='{self.plc_res.text()}' and cardid in (select id from CARDS where marka = '{self.plc_name.text()}'))"
        else:
            select = f"select NAME from ISACARDS WHERE MARKA = '{slovo}'"

        self.cur.execute(select)
        try:
            return [id[0] for id in self.cur][0]
        except:
            return slovo

    def reverce_code(self):
        try:
            self.cur = self.con.cursor()
            new_str = []

            rows_str = self.text.split('\n')
            for string_some in rows_str:
                if string_some == '':
                    new_str.append('')
                    continue

                result = self.find_tempalte(template=r'__EXVAR_\d+', function_str=self.exvar_str,
                                            string_some=string_some, function_get=self.get_card_from_exvar)

                for temlate in [r'_IO_IU[0-9_]+', r'_IO_QU[0-9_]+', r'_IO_IX[0-9_]+', r'_IO_QX[0-9_]+']:
                    result = self.find_tempalte(template=temlate, function_str=self.plus_com,
                                                string_some=result, function_get=self.get_card_from_com)

                new_str.append(result)

            return '\n'.join(new_str)
        except:
            return "Упс, ошибочка вышла :("

    def get_card_from_exvar(self, exvar):

        exvar_num = exvar.split('__EXVAR_')[1]
        select = f"select name from OBJTYPEPARAM  where id in (select objtypeparamid from CARDPARAMS  where id = {exvar_num})"
        self.cur.execute(select)
        try:
            param = [count[0] for count in self.cur][0]
        except:
            param = 'Не найдено'

        if not self.sett_checkbox.isChecked():
            select = f"select MARKA from cards  where id in (select cardid from CARDPARAMS  where id = {exvar_num}) and and plc_id in (select id from CARDS  where MARKA = '{self.plc_name.text()}')"
        else:
            select = f"select MARKA from cards  where id in (select cardid from CARDPARAMS  where id = {exvar_num})"

        self.cur.execute(select)
        try:
            card = [count[0] for count in self.cur][0]
        except:
            card = 'Не найдено'

        return f"{card}.{param}"

    def exvar_str(self, slovo):
        return '{%s}' % slovo

    def plus_com(self, slovo):
        return f'<<{slovo}>>'

    def plus_str(self, some_data):
        return '__EXVAR_' + str(some_data)

    def generat(self):
        try:
            self.cur = self.con.cursor()

            text = []
            rows_str = self.text.split('\n')
            for register in rows_str:
                if register == '':
                    text.append('\n')
                    continue

                new_code_line = self.find_tempalte(template=r'{(.*?)}', function_str=self.plus_str,
                                                   string_some=register, function_get=self.get_id_texobj_param,
                                                   replace_teml='{%s}')

                new_code_line = self.find_tempalte(template=r'<<(.*?)>>', function_str=str,
                                                   string_some=new_code_line, function_get=self.get_com,
                                                   replace_teml='<<%s>>')

                text.append(new_code_line + '\n')

            return ''.join(text)
        except Exception as err:
            return f"Упс, ошибочка вышла :(, {err.__class__}"

    def get_id_texobj(self, name_texobj):
        if not self.sett_checkbox.isChecked():
            select = f"select ID from CARDS where MARKA = '{name_texobj}' and PLC_GR in (select id from RESOURCES where name='{self.plc_res.text()}' and cardid in (select id from CARDS where marka = '{self.plc_name.text()}'))"
        else:
            select = f"select ID from CARDS where MARKA = '{name_texobj}'"

        self.cur.execute(select)

        try:
            id_tex = [id[0] for id in self.cur][0]
        except:
            id_tex = name_texobj
        return id_tex

    def get_id_params(self, texobj_id, param_name):
        if not self.sett_checkbox.isChecked():
            select = f"select CARDPARAMS.ID from CARDPARAMS join OBJTYPEPARAM on CARDPARAMS.OBJTYPEPARAMID = OBJTYPEPARAM.ID " \
                 f"where CARDPARAMS.CARDID = {texobj_id} and  OBJTYPEPARAM.NAME = '{param_name}' and CARDPARAMS.PLC_GR in (select id from RESOURCES where name='{self.plc_res.text()}' and cardid in (select id from CARDS where marka = '{self.plc_name.text()}'))"
        else:
            select = f"select CARDPARAMS.ID from CARDPARAMS join OBJTYPEPARAM on CARDPARAMS.OBJTYPEPARAMID = OBJTYPEPARAM.ID " \
                     f"where CARDPARAMS.CARDID = {texobj_id} and  OBJTYPEPARAM.NAME = '{param_name}'"

        self.cur.execute(select)
        try:
            id_tex = [id[0] for id in self.cur][0]
        except:
            id_tex = param_name
        return id_tex

    def get_id_texobj_param(self, name):
        texobj_name, param_name = name.split('.', 1)
        texobj_id = self.get_id_texobj(texobj_name)
        if texobj_id != texobj_name:
            param_id = self.get_id_params(texobj_id, param_name)
            return param_id
        return param_name

    def get_com(self, name):
        if not self.sett_checkbox.isChecked():
            select = f"select MARKA from ISACARDS WHERE NAME = '{name}' and resid in (select id from RESOURCES where name='{self.plc_res.text()}' and cardid in (select id from CARDS where marka = '{self.plc_name.text()}'))"
        else:
            select = f"select MARKA from ISACARDS WHERE NAME = '{name}'"

        self.cur.execute(select)
        try:
            return [id[0] for id in self.cur][0]
        except:
            return name

    def connect_bd(self, path, server):
        self.con = firebirdsql.connect(
            host=server,
            database=path,
            port=3050,
            user='sysdba',
            password='masterkey',
            charset='utf8'
        )
        self.cur = self.con.cursor()


class Tab(LibTab):
    def __init__(self):
        super().__init__()
        self.rows = []
        self.initData()
        self.initUI()

        self.thread_bd = CloneThread(plc_name=self.plc_line, plc_res=self.plc_resource,
                                     setting=self.ignore_setting)  # This is the thread object

        # self.thread_bd.finished.connect(self.thread_finished)
        self.thread_bd.signal.connect(self.thread_finished)

    def initData(self):
        self.rows = []
        self.main_title = None

    def initUI(self):

        self.text_panel_code = TextEditor(objectName="text3", tooltip='Код для всавки в <b>проект</b>')

        button_except = SimpleBtn(label="Добавить", click_func=self.view_code)
        button_generat = SimpleBtn(label="Сгенерировать", click_func=self.generat)
        button_clean = SimpleBtn(label="Очистить", click_func=self.clean)
        button_reverce = SimpleBtn(label="Обратно", click_func=self.reverce_code)

        self.plc_line = LineText(text='ICore_2', placeholder='plc_name')
        self.plc_resource = LineText(text='Resource1', placeholder='plc_resource')

        self.text_panel = TextEditor(objectName="text1", tooltip='Генерация промежуточного значения', height=200,
                                     text="""['<<[COM999:1:60210] mb_master_hr_real_in_v > канал 1>>',
                                     '{GP0021_SHOL7_QF24_EOFF.Значение}']""")

        self.text_panel_view = TextEditor(objectName="text2", tooltip='Промежуточное значение')

        self.status = QLabel('')
        self.set_status(status="База не открыта", color='#780d04')

        self.ignore_setting = CheckBox(label='Игнорировать')

        self.bd_window = SimpleDBPath(mainwin=self)
        self.bd_window.my_signal.connect(self.BD_is_open)

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.text_panel_code)
        splitter.addWidget(self.text_panel_view)

        splitter_v = QSplitter(Qt.Vertical)
        splitter_v.addWidget(splitter)
        splitter_v.addWidget(self.text_panel)

        self.main_layout.addWidget(splitter_v, 0, 0, 27, 20)

        self.main_layout.addWidget(self.plc_line, 5, 21, 1, 2)
        self.main_layout.addWidget(self.plc_resource, 6, 21, 1, 2)
        self.main_layout.addWidget(self.ignore_setting, 4, 21, 1, 2)

        self.main_layout.addWidget(button_clean, 15, 22, 1, 1)
        self.main_layout.addWidget(button_except, 15, 21, 1, 1)
        self.main_layout.addWidget(self.bd_window, 0, 21, 1, 2)
        self.main_layout.addWidget(button_generat, 16, 21, 1, 2)
        self.main_layout.addWidget(button_reverce, 17, 21, 1, 2)
        self.main_layout.addWidget(self.status, 25, 21, 1, 2)

    def thread_finished(self, result):
        ''' Сигналы из потока '''
        if self.thread_bd.reverce_exv:
            self.text_panel_view.setText(result)
        else:
            self.text_panel_code.setText(result)
        self.set_status(status="Готово", color='#0b5506')

    def BD_is_open(self, path, server):

        self.set_status(status="Ок", color='#0b5506')
        self.thread_bd.connect_bd(path=path, server=server)

    def clean(self):
        self.text_panel_view.setText("")

    def view_code(self):
        try:
            self.connection = eval(self.text_panel.toPlainText())
            text = self.text_panel_view.toPlainText() + '\n'
            for con in self.connection:
                text += con
                text += '\n'
            self.text_panel_view.setText(text)
        except Exception as e:
            QMessageBox().warning(self, "Ошибка", str(e), QMessageBox.Ok,
                                  QMessageBox.Ok)

    def generat(self):
        self.set_status(status="Перевдим ...", color='#0e385e')
        self.thread_bd.text = self.text_panel_view.toPlainText()
        self.thread_bd.reverce_exv = False
        self.thread_bd.start()

    def reverce_code(self):
        self.set_status(status="Перевдим ...", color='#0e385e')
        self.thread_bd.text = self.text_panel_code.toPlainText()
        self.thread_bd.reverce_exv = True
        self.thread_bd.start()

    def set_status(self, color, status):
        self.status.setText(f"""
                               Статус: <b style="color: {color};">{status}</b> 
                               """)
