import sqlite3
import xml.dom.minidom

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget

db_path = 'gui\\scripts\\test.db'


class XmlAnalize(QWidget):
    signal = pyqtSignal()
    error = pyqtSignal(str)
    pages = {}
    exception_page = {'{{LINK}}', '{{MENULINK}}'}

    def __init__(self):
        super().__init__()
        self.connect_to_db()
        # self.start_work(path_xml, name, desc)

    def check_table(self):
        self.cursor.execute("""select * from sqlite_master where name='Templates' and type='table';""")
        if self.cursor.fetchall():
            return False
        return True

    def create_table(self):
        self.cursor.execute("""CREATE TABLE "Templates" (
	"id"	INTEGER NOT NULL UNIQUE,
	"name"	TEXT NOT NULL UNIQUE,
	"desc"	TEXT,
	"ChildButton"	TEXT,
	"ChildButton_dy"	INTEGER,
	"ChildParButton"	TEXT,
	"ChildParButton_dy"	INTEGER,
	"ParentButton"	TEXT,
	"ParentButton_dy"	INTEGER,
	"ColorStyle"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);""")

        # фиксирую коммит
        self.conn.commit()

    def connect_to_db(self, path=db_path):
        self.conn = sqlite3.connect(path)
        self.cursor = self.conn.cursor()
        if self.check_table():
            self.create_table()

    def get_subpages(self, dom):
        itemlist = dom.getElementsByTagName('SUBPAGES')
        return itemlist[0].cloneNode(1)

    def get_coloStyle(self, dom):
        itemlist = dom.getElementsByTagName('COLORSTYLES')
        return itemlist[0].cloneNode(1).toxml()

    def get_all_pages(self, dom):
        pages = {}
        subpages = self.get_subpages(dom)

        itemlist = subpages.getElementsByTagName('OnePage')

        for item in itemlist:
            name = item.getElementsByTagName('NAME')[0].firstChild.nodeValue
            if name not in self.exception_page:
                pages.update({name: item}) if name else None
        return pages

    def static_tempalte(self, item, max_width):
        item.attributes['X'].value = f"{{{{WIDTH + X - {max_width} + {item.attributes['X'].value}}}}}"
        item.attributes['Y'].value = f"{{{{Y + {item.attributes['Y'].value}}}}}"
        item.attributes['GRNUM'].value = "0"

        return item.toxml()

    def dynamic_tempalte(self, item):
        item.attributes['X'].value = f"{{{{X + {item.attributes['X'].value}}}}}"
        item.attributes['Y'].value = f"{{{{Y + {item.attributes['Y'].value}}}}}"
        item.attributes['WIDTH'].value = "{{WIDTH}}"
        item = self.animator_id_replace(item)
        item = self.receptor_id_replace(item)
        return item.toxml()

    def animator_id_replace(self, item):
        for receptor in item.getElementsByTagName('OneAnim'):
            if receptor.attributes['PARAMID'].value != '0':
                receptor.attributes['PARAMID'].value = "{{PAGE_ID}}"
        return item

    def receptor_id_replace(self, item):
        for receptor in item.getElementsByTagName('OneReceptor'):
            if receptor.attributes['PARAM_INT'].value != '0':
                receptor.attributes['PARAM_INT'].value = "{{PAGE_ID}}"
        return item

    def make_templates(self, page_name):
        page = self.pages[page_name]
        elements = []
        content = page.getElementsByTagName('OneLayer')[0]
        max_height = 0
        max_width = 0
        for prim in content.getElementsByTagName('OnePrim'):
            if max_height < int(prim.attributes['HEIGHT'].value) + int(prim.attributes['Y'].value):
                max_height = int(prim.attributes['HEIGHT'].value) + int(prim.attributes['Y'].value)

            if max_width < int(prim.attributes['WIDTH'].value) + int(prim.attributes['X'].value):
                max_width = int(prim.attributes['WIDTH'].value) + int(prim.attributes['Y'].value)

            if prim.attributes['GRNUM'].value == '0':
                elements.append(self.dynamic_tempalte(prim))
            else:
                elements.append(self.static_tempalte(prim, max_width))

        return ['\n'.join(elements), max_height]

    def start_work(self, path, name, desc):
        try:
            with open(path, "r", encoding='UTF-8') as f:
                dom = xml.dom.minidom.parse(path)
                dom.normalize()
                self.pages = self.get_all_pages(dom)
                template_dict = {}

                for name_page in self.pages.keys():
                    template_dict.update({name_page: self.make_templates(name_page)})

                template_dict.update({'colorStyle': self.get_coloStyle(dom)})
                self.add_to_db(name=name, desc=desc, template_dict=template_dict)
                self.signal.emit()
        except Exception as err:
            self.error.emit(f"Упс, ошибочка вышла :(, \n {err.__str__()}")

    def add_to_db(self, name='', desc='', template_dict=None):
        self.cursor.execute(
            f"""INSERT INTO `Templates`  (name, desc, ChildButton, ChildButton_dy, ChildParButton, ChildParButton_dy, ParentButton, ParentButton_dy, ColorStyle)  VALUES('{name}', '{desc}', '{template_dict['ChildButton'][0]}', {template_dict['ChildButton'][1]},'{template_dict['ChildParButton'][0]}', {template_dict['ChildParButton'][1]},'{template_dict['ParentButton'][0]}', {template_dict['ParentButton'][1]}, '{template_dict['colorStyle']}');""")
        self.conn.commit()
        self.conn.close()

# if __name__ == '__main__':
#     xml_analize = XmlAnalize()
