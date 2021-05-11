# -*- coding: cp1251 -*-
import copy
import re
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

        self.text_panel_code = QTextEdit(objectName="text3")
        self.text_panel_code.setToolTip('Код для всавки в <b>проект</b>')

        button_generat = widj_tab1.button_setting("Сгенерировать", self.generat)

        self.width = widj_tab1.lile_label("Ширина", '1920')
        self.width_screen = widj_tab1.lile_label("Высота", '1920')
        self.indent_w = widj_tab1.lile_label("Отступ w", '20')
        self.indent_h = widj_tab1.lile_label("Отступ h", '20')
        self.name_wind = widj_tab1.lile_label_name("Имя", "")

        main_layout.addWidget(self.text_panel_code, 0, 0, 27, 1)

        main_layout.addWidget(self.width_screen, 12, 3, 1, 2)
        main_layout.addWidget(self.width, 13, 3, 1, 2)
        main_layout.addWidget(self.indent_w, 14, 3, 1, 2)
        main_layout.addWidget(self.indent_h, 15, 3, 1, 2)
        main_layout.addWidget(self.name_wind, 11, 3, 1, 2)
        main_layout.addWidget(widj_tab1.line_btn_simple(self), 0, 3, 1, 2)
        main_layout.addWidget(button_generat, 16, 3, 1, 2)

        # self.hide_all()

        self.setLayout(main_layout)

    def reverce_code(self):
        try:
            self.cur = self.con.cursor()
            new_str = ""

            rows_str = self.text_panel_code.toPlainText().split('\n')
            for string_some in rows_str:
                if string_some == '':
                    break

                slovo_pos = re.search(r'__EXVAR_\d+', string_some)
                if slovo_pos is None:
                    new_str += '\n'
                    continue
                slovo = string_some[slovo_pos.start():slovo_pos.end()]

                result = re.sub(r'__EXVAR_\d+', f"Э{self.get_card_from_exvar(slovo)}У", string_some)
                new_str += result + '\n'

            self.text_panel_view.setText(new_str)
        except:
            self.text_panel_view.setText("Упс, ошибочка вышла :(")
            return

    def get_card_from_exvar(self, exvar):

        exvar_num = exvar.split('__EXVAR_')[1]
        select = f"select name from OBJTYPEPARAM  where id in (select objtypeparamid from CARDPARAMS  where id = {exvar_num})"
        self.cur.execute(select)
        try:
            param = [count[0] for count in self.cur][0]
        except:
            param = 'Не найдено'

        select = f"select MARKA from cards  where id in (select cardid from CARDPARAMS  where id = {exvar_num})"
        self.cur.execute(select)
        try:
            card = [count[0] for count in self.cur][0]
        except:
            card = 'Не найдено'

        return f"{card}.{param}"

    def clean(self):
        self.text_panel_view.setText("")

    def generat(self):
        try:
            self.cur = self.con.cursor()

            text = ""
            for register in self.connection:
                name_registers = re.findall(r'Э(.*?)У', register)
                list_of_id = [self.get_id_texobj_param(name_register) for name_register in name_registers]
                new_code_line = copy.deepcopy(register)
                for id_param in list_of_id:
                    pos_name = re.search(r'Э(.*?)У', new_code_line)
                    new_code_line = new_code_line[0:pos_name.start()] + '__EXVAR_' + str(id_param) + new_code_line[
                                                                                                     pos_name.end(): len(
                                                                                                         new_code_line)]
                text += new_code_line + '\n'

            self.text_panel_code.setText(text)
        except:
            self.text_panel_code.setText("Упс, ошибочка вышла :(")
            return

    def get_id_texobj(self, name_texobj):
        select = f"select ID from CARDS where MARKA = '{name_texobj}'"
        self.cur.execute(select)
        return [id[0] for id in self.cur][0]

    def get_id_params(self, texobj_id, param_name):
        select = f"select CARDPARAMS.ID from CARDPARAMS join OBJTYPEPARAM on CARDPARAMS.OBJTYPEPARAMID = OBJTYPEPARAM.ID " \
                 f"where CARDPARAMS.CARDID = {texobj_id} and  OBJTYPEPARAM.NAME = '{param_name}' "
        self.cur.execute(select)
        return [id[0] for id in self.cur][0]

    def get_id_texobj_param(self, name):
        texobj_name, param_name = name.split('.')
        texobj_id = self.get_id_texobj(texobj_name)
        param_id = self.get_id_params(texobj_id, param_name)
        return param_id

    def view_code(self):
        self.connection = eval(self.text_panel.toPlainText())
        text = self.text_panel_view.toPlainText() + '\n'
        for con in self.connection:
            text += con
            text += '\n'
        self.text_panel_view.setText(text)
