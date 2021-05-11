# -*- coding: cp1251 -*-
import collections
import re
from collections import namedtuple

import firebirdsql
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal, QThread
from PyQt5.QtWidgets import *
from jinja2 import BaseLoader
from jinja2 import Environment, FileSystemLoader

from LybPyQT5.widgets.button import SimpleBtn
from LybPyQT5.widgets.db_path import SimpleDBPath
from LybPyQT5.widgets.line_text import LineLabel
from LybPyQT5.widgets.tab import LibTab
from LybPyQT5.widgets.table import TableSimple

row_data = namedtuple('row_data', 'kadr evklass main')


def roundUpToMultiple(number, multiple):
    num = number + (multiple - 1)
    return num - (num % multiple)


class Template_clc:
    __slots__ = ['bloks', 'links', 'dx', 'dy', 'id_0', 'd_id']

    def __init__(self, bloks, links, dx, dy, id_0, d_id):
        self.bloks = bloks
        self.links = links
        self.dx = dx
        self.dy = dy
        self.id_0 = id_0
        self.d_id = d_id


class FBD_Templ:
    """Класс для получения шаблона"""
    __slots__ = ['dx', 'dy', 'cur', 'bloks', 'links', 'bloks_main', 'main', 'intermediate', 'ind_num_max',
                 'ind_num']

    def __init__(self, cur):
        self.prepare_to_new_templ()
        self.cur = cur
        self.templates_init()

    def prepare_to_new_templ(self):
        self.ind_num = None
        self.ind_num_max = None
        self.dx = 0
        self.dy = 0

    def get_Type(self, OBJMSID):
        SELECT = f"select name from ISAOBJ where id = {OBJMSID}"
        self.cur.execute(SELECT)
        return [id[0] for id in self.cur.fetchall()][0]

    def templates_init(self):
        env = Environment(loader=FileSystemLoader('.'))
        self.bloks = env.get_template('templates/tab5/Bloks.html')
        self.links = env.get_template('templates/tab5/Links.html')
        self.bloks_main = env.get_template('templates/tab5/Bloks_Main.html')
        self.main = env.get_template('templates/tab5/MAIN.html')
        self.intermediate = env.get_template('templates/tab5/intermediate.html')

    def get_delta_max(self, X, WIDTH, Y, HEIGHT):
        """Определяем длину и ширину"""
        if X + WIDTH > self.dx:
            self.dx = roundUpToMultiple(X + WIDTH, 50)

        if Y + HEIGHT > self.dy:
            self.dy = roundUpToMultiple(Y + HEIGHT, 50)

    def get_delta_ind_max(self, ind):
        """Определяем ind"""
        if self.ind_num_max is None:
            self.ind_num_max = ind
            self.ind_num = ind
        else:
            if ind < self.ind_num:
                self.ind_num = ind

            if ind > self.ind_num_max:
                self.ind_num_max = ind

    def get_params(self, templid):
        select = f"""select ID,X,Y,WIDTH,HEIGHT,PARAMS,OBJMSID,FIELDSID,CARDID from ISAPAGECONTENTS  where  pageid = {templid}"""
        self.cur.execute(select)
        return self.cur.fetchall()

    def get_coord(self, starting_word):
        list_str = []
        asr = starting_word.split(';')
        for s in asr:
            if s.find('(') == -1:
                break

            x, y = s[s.find("(") + 1:s.find(")")].split(',')
            list_str.append('({{dict.X + %s}},{{dict.Y + %s}});' % (x, y))

        slovo = ''.join(list_str)
        params = f'''{slovo}'''
        return params

    def get_ind_link(self, starting_word):
        asr = starting_word.split('|')
        asr[0] = '{{dict.ID + %s}}' % asr[0]
        slovo = '|'.join(asr)
        params = f'''{slovo}'''
        return params

    def get_prefix(self, CARDID):
        select = f"""select PREFIX from ISACARDSTEMPLATE where id = {CARDID}"""
        self.cur.execute(select)
        try:
            prefix = self.cur.fetchall()[0][0]
        except:
            prefix = ''
        return prefix

    def gen_templ(self, templateid):
        self.prepare_to_new_templ()
        templid = templateid
        if templid == 0:
            return

        parameters = self.get_params(templid)
        list_bloks = []
        list_links = []

        for ID, X, Y, WIDTH, HEIGHT, PARAMS, OBJMSID, FIELDSID, CARDID in parameters:
            if (OBJMSID == 0 or OBJMSID is None) and (FIELDSID == 0 or FIELDSID is None):
                '''Links'''
                PL, HINT, FP, LP, BN, CT, *other = PARAMS.split('\r\n')
                dicr_atr = collections.namedtuple('dicr_atr', ['PL', 'FP', 'LP', 'BN', 'CT'])

                param = dicr_atr(self.get_coord(PL.split('=')[1]), self.get_ind_link(FP.split('=')[1]),
                                 self.get_ind_link(LP.split('=')[1]), BN.split('=')[1],
                                 CT.split('=')[1])
                list_links.append(self.links.render(dict=param))
            else:
                if FIELDSID != 0:
                    '''Other bloks'''
                    dicr_atr = collections.namedtuple('dicr_atr', ['Type', 'ID', 'HEIGHT', 'WIDTH', 'X', 'Y'])
                    Type = self.get_Type(OBJMSID)
                    param = dicr_atr(Type, '{{dict.ID + %s}}' % ID, HEIGHT, WIDTH, '{{dict.X + %s}}' % X,
                                     '{{dict.Y + %s}}' % Y)
                    blok = self.bloks.render(dict=param)
                else:
                    '''Main bloks'''
                    prefix = self.get_prefix(CARDID)

                    dicr_atr = collections.namedtuple('dicr_atr', ['Type', 'ID', 'HEIGHT', 'WIDTH', 'X', 'Y', 'Info'])
                    Type = self.get_Type(OBJMSID)
                    param = dicr_atr(Type, '{{dict.ID + %s}}' % ID, HEIGHT, WIDTH, '{{dict.X + %s}}' % X,
                                     '{{dict.Y + %s}}' % Y,
                                     '{{dict.marka}}%s' % prefix)
                    blok = self.bloks_main.render(dict=param)

                self.get_delta_ind_max(ID)
                self.get_delta_max(X, WIDTH, Y, HEIGHT)
                list_bloks.append(blok)

        links = self.intermediate.render(elements=list_links)
        bloks = self.intermediate.render(elements=list_bloks)
        return Template_clc(bloks, links, self.dx, self.dy, self.ind_num, self.ind_num_max - self.ind_num + 1)


class CloneThread(QThread):
    signal = pyqtSignal('PyQt_PyObject', 'PyQt_PyObject', 'PyQt_PyObject')
    bad_signal = pyqtSignal('PyQt_PyObject')

    def __init__(self, con, marks, x0, y0, xmax):
        QThread.__init__(self)
        self.cur = con.cursor()
        self.marks = marks
        self.x0 = x0
        self.y0 = y0
        self.xmax = xmax

    def get_templid(self, marka):
        select = f"""select TEMPLATEID from CARDS where marka = '{marka}'"""
        self.cur.execute(select)
        return [id[0] for id in self.cur.fetchall()][0]

    # run method gets called when we start the thread
    def run(self):
        try:
            brack = []
            dict_templ = {}
            list_bloks = []
            list_links = []
            ind_current = 1

            x_current = self.x0
            y_current = self.y0
            dx0 = self.x0
            dy = self.y0

            ymax = dy

            generate_templ = FBD_Templ(self.cur)

            for mar in self.marks:
                try:
                    templid = self.get_templid(mar)
                except:
                    brack.append(mar)
                    continue

                if templid == 0:
                    brack.append(mar)
                    continue

                if templid not in dict_templ.keys():
                    dict_templ[templid] = generate_templ.gen_templ(templid)

                templ_cur = dict_templ[templid]
                block = Environment(loader=BaseLoader).from_string(templ_cur.bloks)
                link = Environment(loader=BaseLoader).from_string(templ_cur.links)
                dicr_atr = collections.namedtuple('dicr_atr', ['ID', 'X', 'Y', 'marka'])

                ind = ind_current - templ_cur.id_0
                ind_current += templ_cur.d_id

                param = dicr_atr(ind, x_current, y_current, mar)

                x_current += templ_cur.dx + dx0

                if x_current >= self.xmax:
                    x_current = self.x0
                    y_current += ymax + dy
                    ymax = self.y0
                elif ymax < templ_cur.dy:
                    ymax = templ_cur.dy

                list_bloks.append(block.render(dict=param))
                list_links.append(link.render(dict=param))

            self.signal.emit(list_bloks, list_links, brack)
        except Exception as e:
            self.bad_signal.emit(e)


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

        self.text_panel_code = QTextEdit(objectName="text3")
        self.text_panel_code.setToolTip('Код для всавки в <b>проект</b>')

        button_generat = SimpleBtn(label="Сгенерировать", click_func=self.generat)
        button_view = SimpleBtn(label="Отобразить", click_func=self.view_code)

        self.w_screen = LineLabel("Ширина", '1920')
        self.indent_w = LineLabel("Отступ w", '50')
        self.indent_h = LineLabel("Отступ h", '50')
        self.name_wind = LineLabel("Имя", "PRG_TEST")

        self.table = TableSimple(name=["Блок"])

        self.status = QLabel('')
        self.set_status(status="Неизвестно", color='#0e385e')

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.text_panel_code)
        splitter.addWidget(self.table)

        self.bd_window = SimpleDBPath(mainwin=self)
        self.bd_window.my_signal.connect(self.BD_is_open)

        self.main_layout.addWidget(self.w_screen, 12, 16, 1, 2)

        self.main_layout.addWidget(self.status, 6, 16, 1, 2)
        self.main_layout.addWidget(self.indent_w, 14, 16, 1, 2)
        self.main_layout.addWidget(self.indent_h, 15, 16, 1, 2)
        self.main_layout.addWidget(self.name_wind, 11, 16, 1, 2)
        self.main_layout.addWidget(self.bd_window, 0, 16, 1, 2)
        self.main_layout.addWidget(button_view, 17, 16, 1, 2)
        self.main_layout.addWidget(button_generat, 18, 16, 1, 2)
        self.main_layout.addWidget(splitter, 0, 0, 22, 15)

    def BD_is_open(self, path, server):
        self.con = firebirdsql.connect(
            host=server,
            database=path,
            port=3050,
            user='sysdba',
            password='masterkey',
            charset='utf8'
        )
        self.set_status(status="Ок", color='#0b5506')



    def set_status(self, color, status):
        self.status.setText(f"""
                               Статус: <b style="color: {color};">{status}</b> 
                               """)

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
        except Exception as e:
            self.text_panel_view.setText("Упс, ошибочка вышла :(")
            QMessageBox().warning(self, "Ошибка", str(e), QMessageBox.Ok, QMessageBox.Ok)

    def get_count_of_in_out(self, type_id):
        count = [0, 0]
        for direction in [1, 2]:
            select = f"select count(*) from ISAOBJFIELDS where ISAOBJID in (select id from ISAOBJ where id = {type_id}) and direction = {direction}"
            self.cur.execute(select)
            try:
                count[direction - 1] = [count[0] for count in self.cur][0]
            except:
                pass

        return 20 + max(count) * 20

    def get_type_from_marka(self, marka):
        select = f"select tid from ISACARDS where CARDSID in (select id from CARDS where marka = '{marka}')"
        self.cur.execute(select)
        return [id[0] for id in self.cur][0]

    def get_type_name(self, type_id):
        select = f"select name from ISAOBJ where id = {type_id}"
        self.cur.execute(select)
        return [id[0] for id in self.cur][0]

    def get_temp(self, marka):
        type_id = self.get_type_from_marka(marka)
        height = self.get_count_of_in_out(type_id)
        type_name = self.get_type_name(type_id)
        weight = 100 + len(type_name) * 10
        return height, weight, type_name

    # def generat(self):
    #     try:
    #         self.cur = self.con.cursor()
    #
    #         template_num = []
    #         env1 = Environment(loader=FileSystemLoader('.'))
    #         template_num.append(env1.get_template('templates/fbd_xml/block_xml.html'))
    #         env = Environment(loader=FileSystemLoader('.'))
    #         template = env.get_template('templates/fbd_xml/temp_xml.html')
    #         page = []
    #         x0 = 50
    #         y0 = 50
    #         dx0 = int(self.indent_w.line_edit.text())
    #         dy = int(self.indent_h.line_edit.text())
    #         dx = dx0
    #         y = y0
    #         x = x0
    #         ymax = int(self.heigh_screen.line_edit.text())
    #         marks = self.data_row
    #
    #         for marka in marks:
    #             height, weight, type_name = self.get_temp(marka)
    #             con = dict(x=x, y=y, WIDTH=weight, HEIGHT=height, type=type_name, marka=marka)
    #             page.append(str(template_num[0].render(name_page=self.name_wind.line_edit.text(), con=con)))
    #             y += height + dy
    #             if weight + dx0 > dx:
    #                 dx = weight + dx0
    #             if y >= ymax:
    #                 y = y0
    #                 x += dx
    #                 dx = dx0
    #
    #         options = QFileDialog.Options()
    #         options |= QFileDialog.DontUseNativeDialog
    #         fileName, _ = QFileDialog.getSaveFileName(self, "Сохранить xml", "", "xml (*.xml)", options=options)
    #
    #         if fileName == '':
    #             return
    #
    #         if fileName.find('.xml') == -1:
    #             fileName += '.xml'
    #         with open(fileName, "w", encoding='utf8') as f:
    #             f.write(template.render(blocks=page))
    #
    #
    #     except Exception as e:
    #         self.text_panel_code.setText("Упс, ошибочка вышла :(")
    #         QMessageBox().warning(self, "Ошибка", str(e), QMessageBox.Ok, QMessageBox.Ok)
    #         return

    def generat(self):
        try:
            self.cur = self.con.cursor()
            marks = [self.table.item(row, 0).text() for row in range(self.table.rowCount())]
            x0 = int(self.indent_w.line_edit.text())
            y0 = int(self.indent_h.line_edit.text())
            xmax = int(self.w_screen.line_edit.text())

            self.thread_bd = CloneThread(self.con, marks, x0, y0, xmax)  # This is the thread object
            self.thread_bd.signal.connect(self.thread_finished)
            self.thread_bd.bad_signal.connect(self.bad_finished)
            self.thread_bd.start()
            self.set_status(status="Перевдим ...", color='#0e385e')

        except Exception as e:
            QMessageBox().warning(self, "Ошибка", str(e), QMessageBox.Ok, QMessageBox.Ok)
            self.set_status(status="Ошибка", color='#780d04')
            return

    def bad_finished(self, error):
        QMessageBox().warning(self, "Ошибка", str(error), QMessageBox.Ok, QMessageBox.Ok)
        self.set_status(status="Ошибка", color='#780d04')

    def thread_finished(self, list_bloks, list_links, brack):
        ''' Сигналы из потока '''
        self.set_status(status="OK", color='#0b5506')
        env = Environment(loader=FileSystemLoader('.'))
        main = env.get_template('templates/tab5/MAIN.html')

        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "Сохранить xml", "", "xml (*.xml)", options=options)
        if fileName == '':
            return
        if fileName.find('.xml') == -1:
            fileName += '.xml'
        with open(fileName, "w", encoding='utf8') as f:
            f.write(main.render(bloks=list_bloks, links=list_links, name=self.name_wind.line_edit.text()))

        if len(brack) != 0:
            QMessageBox().warning(self, "Не удалось найти",
                                  'Следующие блоки отсутствуют:           \n' + str(', '.join(brack)), QMessageBox.Ok,
                                  QMessageBox.Ok)

        self.set_status(status="Готово", color='#0b5506')

    def view_code(self):
        data_row = []
        text_code = self.text_panel_code.toPlainText().split('\n')
        self.table.setRowCount(0)
        for text in text_code:
            block = text.split('.')
            if len(block) > 1 and block[0] not in data_row:
                index = self.table.rowCount()
                self.table.setRowCount(index + 1)  # и одну строку в таблице
                self.table.setItem(index, 0, QTableWidgetItem(block[0]))
                data_row.append(block[0])
