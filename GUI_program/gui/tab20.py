# -*- coding: cp1251 -*-

import xml.dom.minidom

from PyQt5.QtCore import QMimeData, Qt
from PyQt5.QtGui import *
from PyQt5.QtGui import QDrag, QPixmap, QPainter
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QGridLayout, QLabel, QWidget, QLineEdit, QApplication

import gui.widgets.widj_tab1 as widj_tab1


class DraggableLabel(QLabel):
    def __init__(self, *args, **kwargs):
        QLabel.__init__(self, *args, **kwargs)

        self.setAlignment(Qt.AlignCenter)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.pos()

    def mouseMoveEvent(self, event):
        if not (event.buttons() & Qt.LeftButton):
            return
        if (event.pos() - self.drag_start_position).manhattanLength() < QApplication.startDragDistance():
            return
        drag = QDrag(self)
        mimedata = QMimeData()
        mimedata.setText(self.text())
        drag.setMimeData(mimedata)
        pixmap = QPixmap(self.size())
        painter = QPainter(pixmap)
        painter.drawPixmap(self.rect(), self.grab())
        painter.end()
        drag.setPixmap(pixmap)
        drag.setHotSpot(event.pos())
        drag.exec_(Qt.CopyAction | Qt.MoveAction)


class Template:

    def __init__(self):
        self.properties_drop = {}

    def old_property(self, dom):
        self.properties_drop = {}
        itemlist = dom.getElementsByTagName('OBJTYPE')
        for item in itemlist:
            try:
                flag_continue = False
                for group in item.getElementsByTagName('ISGROUP'):
                    if group.childNodes[0].data == '1':
                        flag_continue = True
                        break
                if not flag_continue:
                    for param in item.getElementsByTagName('OBJTYPEPARAMS')[0].getElementsByTagName('PARAM'):
                        self.properties_drop[param.getAttribute("Name")] = param.toxml()
            except Exception as e:
                print('Failed to upload to ftp: ' + str(e))

        return self.properties_drop.keys()

    def open_xml(self, path):

        with open(path, "r", encoding='UTF-8') as f:
            contents = f.read()
            dom = xml.dom.minidom.parseString(contents)
            dom.normalize()

            return self.old_property(dom)

    def property(self, dom):
        properties = []
        itemlist = dom.getElementsByTagName('OBJTYPE')
        for item in itemlist:
            try:
                flag_continue = False
                for group in item.getElementsByTagName('ISGROUP'):
                    if group.childNodes[0].data == '1':
                        flag_continue = True
                        break
                if not flag_continue:
                    for param in item.getElementsByTagName('OBJTYPEPARAMS')[0].getElementsByTagName('PARAM'):
                        if param.getElementsByTagName('DISC')[0].firstChild is not None:
                            disc = param.getElementsByTagName('DISC')[0].firstChild.data
                        else:
                            disc = 'None'
                        properties.append([param.getAttribute("Name"), disc])
            except Exception as e:
                print('Failed to upload to ftp: ' + str(e))

        return properties

    def new_property(self, dom, dict_property):
        flag_continue = False
        replace_list = []
        while len(dict_property.keys()) != len(replace_list):
            itemlist = dom.getElementsByTagName('OBJTYPE')
            for item in itemlist:
                try:
                    flag_continue = False
                    for group in item.getElementsByTagName('ISGROUP'):
                        if group.childNodes[0].data == '1':
                            flag_continue = True
                            break
                    if not flag_continue:
                        for param in item.getElementsByTagName('OBJTYPEPARAMS')[0].getElementsByTagName('PARAM'):
                            if param.getAttribute("Name") not in replace_list and param.getAttribute(
                                    "Name") in dict_property.keys():
                                replace_list.append(param.getAttribute("Name"))
                                NAME = param.getAttribute("Name")
                                DICT = dict_property[NAME][1]
                                ID = param.getAttribute("ID")
                                PID = param.getElementsByTagName('PID')[0].childNodes[0].data
                                try:
                                    PLC_VARNAME = param.getElementsByTagName('PLC_VARNAME')[0].childNodes[0].data
                                except:
                                    PLC_VARNAME = None
                                PGROUPID = param.getElementsByTagName('PGROUPID')[0].childNodes[0].data
                                new_property = self.prepare_new_prop(PGROUPID, DICT, NAME, ID, PID, PLC_VARNAME,
                                                                     self.properties_drop[dict_property[NAME][0]])
                                old_property = param.toxml()
                                dom = self.replace_property(dom, old_property, new_property)
                                break

                except Exception as e:
                    print('Failed to upload to ftp: ' + str(e))

                finally:
                    if not flag_continue:
                        break
        # return dom.toxml()
        return dom

    def replace_property(self, dom, old_property, new_property):
        dom = xml.dom.minidom.parseString(dom.toxml().replace(old_property, new_property))
        return dom

    def prepare_new_prop(self, PGROUPID, DICT, NAME, ID, PID, PLC_VARNAME, data_xml):
        dom = xml.dom.minidom.parseString(data_xml)
        dom.normalize()
        if DICT == 'None':
            DICT = ''
        dom.getElementsByTagName('PGROUPID')[0].childNodes[0].data = PGROUPID
        dom.getElementsByTagName("PARAM")[0].setAttribute("Name", NAME)
        dom.getElementsByTagName("PARAM")[0].setAttribute("ID", ID)
        dom.getElementsByTagName('PID')[0].childNodes[0].data = PID
        dom.getElementsByTagName('NAME')[0].childNodes[0].data = NAME
        dom.getElementsByTagName('ID')[0].childNodes[0].data = ID
        if PLC_VARNAME:
            dom.getElementsByTagName('PLC_VARNAME')[0].childNodes[0].data = PLC_VARNAME

        if dom.getElementsByTagName('DISC')[0].firstChild is None:
            node = dom.getElementsByTagName('DISC')[0]
            # replaceText(node, "Hello World")
            new_data = dom.createTextNode(DICT)
            node.appendChild(new_data)
        else:
            dom.getElementsByTagName('DISC')[0].childNodes[0].data = DICT

        return dom.getElementsByTagName("PARAM")[0].toxml()

    def open_new_xml(self, path):
        with open(path, "r", encoding='UTF-8') as f:
            contents = f.read()
            dom = xml.dom.minidom.parseString(contents)
            dom.normalize()
            self.new_xml = dom.toxml()
            return self.property(dom)

    def new_property_only(self, dom, dict_property):
        flag_continue = False

        itemlist = dom.getElementsByTagName('OBJTYPE')
        for item in itemlist:
            try:
                flag_continue = False
                for group in item.getElementsByTagName('ISGROUP'):
                    if group.childNodes[0].data == '1':
                        flag_continue = True
                        break
                if not flag_continue:
                    for param in item.getElementsByTagName('OBJTYPEPARAMS')[0].getElementsByTagName('PARAM'):
                        if param.getAttribute("Name") in dict_property.keys():
                            if param.getElementsByTagName('DISC')[0].firstChild is None:
                                node = param.getElementsByTagName('DISC')[0]
                                # replaceText(node, "Hello World")
                                new_data = dom.createTextNode(dict_property[param.getAttribute("Name")])
                                node.appendChild(new_data)
                            else:
                                param.getElementsByTagName('DISC')[0].childNodes[0].data = dict_property[
                                    param.getAttribute("Name")]

            except Exception as e:
                print('Failed to upload to ftp: ' + str(e))

        # return dom.toxml()
        return dom

    def generate_xml(self, path, dict_property):
        with open(path, "w", encoding='utf8') as f:
            dom = xml.dom.minidom.parseString(self.new_xml)
            dom.normalize()
            new_dom = self.new_property(dom, dict_property)

            new_dom.writexml(f, encoding="UTF-8")
            f.close()

    def generate_only_xml(self, path, dict_property):
        with open(path, "w", encoding='utf8') as f:
            dom = xml.dom.minidom.parseString(self.new_xml)
            dom.normalize()
            new_dom = self.new_property_only(dom, dict_property)

            new_dom.writexml(f, encoding="UTF-8")
            f.close()


class DropLabel(QLabel):
    def __init__(self, *args, **kwargs):
        QLabel.__init__(self, *args, **kwargs)
        self.setAcceptDrops(True)
        self.setAlignment(Qt.AlignCenter)

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event):
        pos = event.pos()
        text = event.mimeData().text()
        self.setText(text)
        event.acceptProposedAction()


class DropItem(QTableWidgetItem):
    def __init__(self, text):
        super().__init__(text)

    def dropEvent(self, event):
        text = event.mimeData().text()
        self.setText(text)
        event.acceptProposedAction()


class DropWidjet(QWidget):
    def __init__(self, text):
        super().__init__()

        self.nameLabel = DropLabel(text)
        self.nameLabel.setMinimumHeight(100)
        self.mainLayout = QGridLayout()
        self.mainLayout.addWidget(self.nameLabel, 0, 0)
        self.setMinimumHeight(100)
        self.setLayout(self.mainLayout)
        self.nameLabel.setAlignment(Qt.AlignCenter)
        #
        # self.setWindowTitle("Right-click to edit the name")

    #     self.create_actions()
    #     self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
    #     self.customContextMenuRequested.connect(self.setup_context_menu)
    #     self.setMinimumHeight(60)
    # def create_actions(self):
    #     self.startEditAct = QAction('Edit', self, triggered=self.start_edit_name)
    #
    # def setup_context_menu(self, point):
    #     aMenu = QMenu()
    #     aMenu.addAction(self.startEditAct)
    #     aMenu.exec_(self.mapToGlobal(point))

    def mouseDoubleClickEvent(self, a0: QMouseEvent):
        self.nameEdit = QLineEdit(self.nameLabel.text())
        self.mainLayout.addWidget(self.nameEdit, 0, 0)
        self.nameEdit.returnPressed.connect(self.finish_edit_name)

    def finish_edit_name(self):
        self.nameLabel.setText(self.nameEdit.text())
        self.nameEdit.hide()


class Tab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.new_templates = Template()
        self.properties_drop = {}

    def initUI(self):

        main_layout = QGridLayout()

        self.table = widj_tab1.table_setting_drag(["Каналы", "Описание", "Свойства"])

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)  # ResizeToContents)

        self.table1 = widj_tab1.table_setting_drop(["Каналы"])

        button_open_source = widj_tab1.button_setting("Открыть файл источник", self.open_xml)
        button_open_receptor = widj_tab1.button_setting("Открыть файл для эксп.", self.open_xml_new)
        button_save = widj_tab1.button_setting("Сгенерировать", self.generate_xml)

        # Пустота
        # main_layout.setColumnStretch(10, 4)

        self.only_disc = widj_tab1.check_box_line('Только описание')
        # self.only_disc.cb.setChecked(True)

        main_layout.addWidget(self.table1, 0, 11, 30, 6)
        main_layout.addWidget(self.table, 0, 0, 30, 10)

        main_layout.addWidget(button_open_source, 3, 17, 1, 1)
        main_layout.addWidget(button_open_receptor, 4, 17, 1, 1)
        main_layout.addWidget(button_save, 9, 17, 1, 1)
        main_layout.addWidget(self.only_disc, 6, 17, 1, 1)

        self.setLayout(main_layout)

    def generate_xml(self):
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "Сохранить xml", "", "xml (*.xml)", options=options)

        if fileName == '':
            return

        if fileName.find('.xml') == -1:
            fileName += '.xml'

        if not self.only_disc.cb.isChecked():
            dict_of_property = {
                self.table.item(row, 0).text(): [self.table.item(row, 2).text(), self.table.item(row, 1).text()]
                for row in range(self.table.rowCount()) if self.table.item(row, 2).text() != 'None'}
            self.new_templates.generate_xml(fileName, dict_of_property)
        else:
            dict_of_property = {self.table.item(row, 0).text(): self.table.item(row, 1).text() for row in
                                range(self.table.rowCount()) if self.table.item(row, 1).text() != 'None'}
            self.new_templates.generate_only_xml(fileName, dict_of_property)

    def open_xml(self):
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        path, _ = QFileDialog.getOpenFileName(self, 'Открыть xml', "", "Xml (*.xml)", options=options)

        if path == '':
            return

        try:

            self.properties_drop = self.new_templates.open_xml(path)
            self.table1.setRowCount(len(self.properties_drop))  # и одну строку в таблице

            for ind, key in enumerate(self.properties_drop):
                self.table1.setItem(ind, 0, QTableWidgetItem(key))

        except Exception as e:
            QMessageBox().warning(self, "Ошибка", str(e), QMessageBox.Ok, QMessageBox.Ok)

    def open_xml_new(self):
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        path, _ = QFileDialog.getOpenFileName(self, 'Открыть xml', "", "Xml (*.xml)", options=options)

        if path == '':
            return

        try:

            self.properties_drag = self.new_templates.open_new_xml(path)
            self.table.setRowCount(len(self.properties_drag))  # и одну строку в таблице

            for ind, [property, disc] in enumerate(self.properties_drag):
                self.table.setItem(ind, 0, QTableWidgetItem(property))
                self.table.setItem(ind, 2, QTableWidgetItem('None'))
                self.table.setItem(ind, 1, QTableWidgetItem(disc))


        except Exception as e:
            QMessageBox().warning(self, "Ошибка", str(e), QMessageBox.Ok,
                                  QMessageBox.Ok)

#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     w = Tab()
#     w.show()
#     sys.exit(app.exec_())
