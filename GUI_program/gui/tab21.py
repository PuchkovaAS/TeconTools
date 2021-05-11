# -*- coding: cp1251 -*-

import xml.dom.minidom

from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QGridLayout, QWidget

import gui.widgets.widj_tab1 as widj_tab1


class Template:

    def __init__(self):
        self.object_name = {}

    def list_of_piture(self, dom):
        list_picture = []
        itemlist = dom.getElementsByTagName('MSONE')
        for item in itemlist:
            if item.getAttribute("isMS") == "4":
                list_picture.append(item.getAttribute("Name"))
        return list_picture

    def old_property(self, cadrname):
        dom = self.dom
        self.object_name = {}
        alllist = dom.getElementsByTagName('MSONE')
        for cadr in alllist:
            if cadr.getAttribute("Name") != cadrname:
                continue

            itemlist = cadr.getElementsByTagName('grprim')
            for item in itemlist:
                try:
                    for param in item.getElementsByTagName('MSANIMATOR')[0].getElementsByTagName('anim'):
                        self.object_name[item.getElementsByTagName('NAME')[0].childNodes[0].data] = \
                            param.getElementsByTagName('PARAMID')[0].childNodes[0].data

                except Exception as e:
                    print('Failed to upload to ftp: ' + str(e))

        return self.object_name

    def open_xml(self, path):

        with open(path, "r", encoding='UTF-8') as f:
            contents = f.read()
            self.dom = xml.dom.minidom.parseString(contents)
            self.dom.normalize()
            list_picture = self.list_of_piture(self.dom)
            return list_picture

    def new_property(self, dom, dict_property, cardname):

        for property in dict_property.keys():

            alllist = dom.getElementsByTagName('MSONE')
            for cadr in alllist:
                if cadr.getAttribute("Name") != cardname:
                    continue
                itemlist = cadr.getElementsByTagName('grprim')
                for item in itemlist:
                    try:
                        if item.getElementsByTagName('NAME')[0].childNodes[0].data != property:
                            continue

                        for param in item.getElementsByTagName('MSANIMATOR')[0].getElementsByTagName('anim'):
                            param.getElementsByTagName('PARAMID')[0].childNodes[0].data = dict_property[property]


                    except Exception as e:
                        print('Failed to upload to ftp: ' + str(e))

        return dom

    def generate_xml(self, path, dict_property, card):
        with open(path, "w", encoding='utf8') as f:
            new_dom = self.new_property(self.dom, dict_property, card)

            new_dom.writexml(f, encoding="UTF-8")
            f.close()


class Tab(QWidget):
    def __init__(self):
        super().__init__()
        self.new_templates = Template()
        self.initUI()

    def initUI(self):

        main_layout = QGridLayout()

        self.table = widj_tab1.table_setting(["ObjectName", "PARAMID"])
        self.table.setRowCount(1)
        self.table.setItem(0, 1, QTableWidgetItem('None'))
        self.table1 = widj_tab1.table_setting(["ObjectName", "PARAMID"])

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)  # ResizeToContents)

        button_open_source = widj_tab1.button_setting("Открыть исходный файл", self.open_xml)
        button_save = widj_tab1.button_setting("Сгенерировать", self.generate_xml)

        self.combo = QComboBox(self)
        self.combo.activated[str].connect(self.comboChange)

        # main_layout.setColumnStretch(10, 4)

        # self.only_disc.cb.setChecked(True)

        main_layout.addWidget(self.table1, 0, 11, 30, 6)
        main_layout.addWidget(self.table, 0, 0, 30, 10)

        main_layout.addWidget(button_open_source, 3, 17, 1, 1)
        main_layout.addWidget(button_save, 9, 17, 1, 1)
        main_layout.addWidget(self.combo, 15, 17, 1, 1)

        self.setLayout(main_layout)

    def comboChange(self, text):
        self.object_name = self.new_templates.old_property(text)
        self.table1.setRowCount(len(self.object_name))  # и одну строку в таблице

        for ind, key in enumerate(self.object_name):
            self.table1.setItem(ind, 0, QTableWidgetItem(key))
            self.table1.setItem(ind, 1, QTableWidgetItem(self.object_name[key]))

    def generate_xml(self):
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "Сохранить xml", "", "xml (*.xml)", options=options)

        if fileName == '':
            return

        if fileName.find('.xml') == -1:
            fileName += '.xml'

        dict_of_property = {self.table.item(row, 0).text(): self.table.item(row, 1).text()
                            for row in range(self.table.rowCount()) if
                            type(self.table.item(row, 1)) == QTableWidgetItem and self.table.item(row,
                                                                                                  1).text() != 'None'}
        self.new_templates.generate_xml(fileName, dict_of_property, self.combo.currentText())

    def open_xml(self):
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        path, _ = QFileDialog.getOpenFileName(self, 'Открыть xml', "", "Xml (*.xml)", options=options)

        if path == '':
            return

        try:

            cadr_list = self.new_templates.open_xml(path)
            self.object_name = self.new_templates.old_property(cadr_list[0])

            self.combo.clear()
            for cadr in cadr_list:
                self.combo.addItem(cadr)

            self.table1.setRowCount(len(self.object_name))  # и одну строку в таблице

            for ind, key in enumerate(self.object_name):
                self.table1.setItem(ind, 0, QTableWidgetItem(key))
                self.table1.setItem(ind, 1, QTableWidgetItem(self.object_name[key]))

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
