import os
import pickle
import re
import sqlite3
from dataclasses import dataclass

import firebirdsql




class Check_Marka:
    ID_ISA = None
    ID_TO = None

    def __init__(self, marka, ID_TO, cursor):
        self.marka = marka
        self.cursor = cursor
        self.ID_TO = ID_TO
        self.find_ID_ISA()

    def find_ID_ISA(self):
        self.cursor.execute(f"""select ID from ISACARDS where cardsid = {self.ID_TO}""")
        try:
            self.ID_ISA = self.cursor.fetchall()[0][0]
        except:
            self.ID_ISA = None

    def find_pages(self, pages):
        self.cursor.execute(f"""select pageid from PAGECONTENTS where CARDID = {self.ID_TO}""")
        result = self.cursor.fetchall()
        pages_name = [pages.pages_dict_SQL[ID[0]].NAME for ID in result]
        if pages_name:
            return '\n--------\n'.join(pages_name)
        return 'None'

    def find_ISA_pages(self, isa_pages):
        if self.ID_ISA:
            self.cursor.execute(f"""select pageid from ISAPAGECONTENTS where CARDID = {self.ID_ISA}""")
            result = self.cursor.fetchall()
            pages_name = [isa_pages.pages_dict_SQL[ID[0]].NAME for ID in result]
            if pages_name:
                return '\n--------\n'.join(pages_name)
        return 'None'


@dataclass
class Page:
    ID: int = 0
    PID: int = 0
    NAME: str = ''


class PagesStruct:

    def __init__(self, cursor):
        self.pages_dict_SQL = {}
        self.cursor = cursor
        self.get_all_pages()
        self.get_struct_pages()

    def get_all_pages(self):
        self.cursor.execute(f"""select ID, PID, NAME from GRPAGES""")
        self.pages_dict_SQL = {ID: Page(ID=ID, PID=PID, NAME=NAME) for ID, PID, NAME in self.cursor.fetchall()}

    def get_struct_pages(self):
        for page in self.pages_dict_SQL.values():
            while True:
                try:
                    parent = self.pages_dict_SQL[page.PID]
                    page.PID = parent.PID
                    page.NAME = f"{parent.NAME}//{page.NAME}"
                except:
                    break


class ISAPagesStruct(PagesStruct):
    def __init__(self, cursor):
        super().__init__(cursor)
        self.get_resources()
        self.add_resource()

    def get_all_pages(self):
        self.cursor.execute(f"""select ID, GROUPID, NAME from ISAOBJ where kindobj = 6""")
        self.pages_dict_SQL = {ID: Page(ID=ID, PID=PID, NAME=NAME) for ID, PID, NAME in self.cursor.fetchall()}

    def get_resources(self):
        self.cursor.execute(
            f"""SELECT ISAOBJ.ID, CARDS.MARKA, CARDS.ID, RESOURCES.NAME  FROM ISAOBJ JOIN ISAPOUSTTEXT ON 
ISAPOUSTTEXT.ISAOBJID=ISAOBJ.ID JOIN RESOURCES ON RESOURCES.ID = ISAPOUSTTEXT.RESOURCE JOIN CARDS ON 
RESOURCES.CARDID = CARDS.ID   where ISAOBJ.KINDOBJ = 6 """)
        response = self.cursor.fetchall()
        self.resource_dict = {ID: f'{MARKA}//{NAME}' for ID, MARKA, ID_M, NAME in response}

        self.reverce_resource_dict = {f'{MARKA}//{NAME}': ID_M for ID, MARKA, ID_M, NAME in response}

    def add_resource(self):
        for page in self.pages_dict_SQL.values():
            page.NAME = f'{self.resource_dict[page.ID]}//{page.NAME}'


class KlassStruct(PagesStruct):
    def get_all_pages(self):
        self.cursor.execute(f"""select ID, PID, NAME from KLASSIFIKATOR""")
        self.pages_dict_SQL = {ID: Page(ID=ID, PID=PID, NAME=NAME) for ID, PID, NAME in self.cursor.fetchall()}


class EvklassStruct(PagesStruct):
    def get_all_pages(self):
        self.cursor.execute(f"""select ID, PID, NAME from EVKLASSIFIKATOR""")
        self.pages_dict_SQL = {ID: Page(ID=ID, PID=PID, NAME=NAME) for ID, PID, NAME in self.cursor.fetchall()}


class ST_text_analyze:

    def __init__(self, cursor):
        self.cursor = cursor

    def get_all_st(self, isa_pages):
        self.isa_pages = isa_pages
        select = f"""SELECT ISAOBJ.ID, ISAPOUSTTEXT.DATA FROM ISAOBJ JOIN ISAPOUSTTEXT ON 
ISAPOUSTTEXT.ISAOBJID=ISAOBJ.ID where ISAOBJ.KINDOBJ = 6 and ISAOBJ.ID NOT IN (SELECT ISAOBJ.ID FROM ISAOBJ JOIN 
ISAPOUSTTEXT ON ISAPOUSTTEXT.ISAOBJID=ISAOBJ.ID JOIN ISAGRPAGES ON ISAGRPAGES.ID=ISAOBJ.ID where ISAOBJ.KINDOBJ = 6) """
        self.cursor.execute(select)
        self.st_code = [[isa_pages.pages_dict_SQL[ID].NAME, DATA] for ID, DATA in self.cursor.fetchall()]

        self.cursor.execute("select MARKA from CARDS")
        self.all_marks = set(MARKA[0] for MARKA in self.cursor.fetchall())

        self.result_dict = {}

        for page, text in self.st_code:
            self.union_marks(self.reverce_code(text, page), page)

        return self.result_dict

    def union_marks(self, new_result, page):
        for marka in new_result:
            current = self.result_dict.get(marka, [])
            current.append(page)
            self.result_dict[marka] = current

    def clean_code(self, some_code):
        """Очищаем от комментов"""

        pass_code = False
        if some_code[0:2] == '//':
            pass_code = True

        template_1 = '(*'
        open_comment = some_code.split(template_1)
        template_2 = '*)'
        close_comment = some_code.split(template_2)
        if open_comment != close_comment:
            self.pass_multucode = len(open_comment) > len(close_comment)

        return pass_code or self.pass_multucode

    def find_id_card(self, MARKA, page):

        PLC, RES, *kwar = page.split('//')
        PLC_ID = self.isa_pages.reverce_resource_dict[f'{PLC}//{RES}']
        self.cursor.execute(f"""select ID from CARDS where MARKA = '{MARKA}' and PLC_ID = {PLC_ID}""")
        try:
            ID_MARKA = self.cursor.fetchall()[0][0]
        except:
            ID_MARKA = None
        return ID_MARKA

    def find_tempalte(self, template, function_str, function_get, string_some, replace_teml='%s', page=''):

        template_1 = r'\w+[\. (>=<:);,]'
        name_registers = re.findall(template_1, string_some)

        list_of_id1 = set()
        for name_register in name_registers:
            if name_register[0:-1] not in self.all_marks:
                continue
            ID_MARKA = self.find_id_card(MARKA=name_register[0:-1], page=page)
            list_of_id1.add(ID_MARKA)

        list_of_id = set()
        name_registers = re.findall(template, string_some)
        for name_register in name_registers:
            ID_MARKA = function_get(name_register)
            list_of_id.add(ID_MARKA)

        return list_of_id1.union(list_of_id)

    def exvar_str(self, slovo):
        return '{%s}' % slovo

    def reverce_code(self, text, page):
        try:
            stcode_marcs = set()
            self.pass_multucode = False
            rows_str = text.split('\n')
            for string_some in rows_str:
                if string_some == '':
                    continue
                # string_some = ''.join(string_some.split())
                if not self.clean_code(string_some):
                    result = self.find_tempalte(template=r'__EXVAR_\d+', function_str=self.exvar_str,
                                                string_some=string_some, function_get=self.get_card_from_exvar,
                                                page=page)
                    if result:
                        stcode_marcs = stcode_marcs.union(result)

            return stcode_marcs
        except:
            # raise ValueError("err.__str__()")
            return "Упс, ошибочка вышла :("

    def get_card_from_exvar(self, exvar):

        exvar_num = exvar.split('__EXVAR_')[1]

        select = f"select cardid from CARDPARAMS  where id = {exvar_num}"
        self.cursor.execute(select)
        try:
            card = [count[0] for count in self.cursor][0]
        except:
            card = None

        return card


class DB_Result:
    name_db = 'result2.db'
    path_db_res = os.path.join(os.getcwd(), name_db)

    # __slots__ = []

    def __init__(self, path_result, path_fbd, server):
        self.path_fbd = path_fbd
        self.server = server
        if os.path.exists(path_result):
            try:
                os.remove(path_result)
            except OSError:
                # print('База открыта')
                raise ValueError("База открыта")
                exit()

        self.conn = sqlite3.connect(path_result)
        """ Создание БД в памяти """
        # self.conn = sqlite3.connect(':memory:')
        self.cursor = self.conn.cursor()
        self.create_new_table()

    def create_new_table(self):
        # создание таблиц
        self.cursor.executescript("""
        			BEGIN TRANSACTION;
        			CREATE TABLE "ResultTable" (
        				`id`    INTEGER PRIMARY KEY AUTOINCREMENT,
        				`id_marka`    INTEGER,   
        				`Marka`    TEXT,
        				`KLASS`    TEXT,
        				`TYPE`    TEXT,
        				`PLC_NAME`    TEXT,
        				`ISA`    BOOLEAN,
        				`Pages`    TEXT,
        				`ISA_Pages`    TEXT,
        				`ST_prog`    TEXT
        			);
        			
        			CREATE TABLE "AdditionalTable" (
	"id_marka"	INTEGER,
	"NAME"	TEXT,
	"DISC"	TEXT,
	"OBJSIGN"	TEXT,
	"OBJNUMBER"	TEXT,
	"PLC_VARNAME"	TEXT,
	"ARH_PER"	TEXT,
	"KKS"	TEXT,
	"OBJDPARAM"	TEXT,
	"SREZCONTROL"	TEXT,
	"EVGROUP"	TEXT,
	"PLC_ADRESS"	TEXT,
	"PLC_GR"	TEXT,
	"TEMPLATE"	TEXT,
	FOREIGN KEY("id_marka") REFERENCES "ResultTable"("id_marka")
);

        			COMMIT;
        		""")

        # фиксирую коммит
        self.conn.commit()

    def analyze_text(self, isa_pages, save_file):
        st_analyze = ST_text_analyze(self.fdb_cur)
        resul_st_code = st_analyze.get_all_st(isa_pages)
        f = open(save_file, 'wb')
        pickle.dump(resul_st_code, f)  # помещаем объект в файл
        f.close()
        return resul_st_code

    def not_analyze_text(self, save_file):
        f = open(save_file, 'rb')
        resul_st_code = pickle.load(f)
        return resul_st_code

    def firebird_db_init(self):
        self.fdb_conn = firebirdsql.connect(
            host=self.server,
            database=self.path_fbd,
            port=3050,
            user='sysdba',
            password='masterkey',
            charset='utf8'
        )
        self.fdb_cur = self.fdb_conn.cursor()

        # определение страниц кода и кадров

        pages = PagesStruct(self.fdb_cur)
        isa_pages = ISAPagesStruct(self.fdb_cur)

        # определяем классификаторы
        klid = KlassStruct(self.fdb_cur)

        # определяем классификаторы
        self.evklid = EvklassStruct(self.fdb_cur)

        save_file = 'resul_st_code.data'
        # анализ st кода
        resul_st_code = self.analyze_text(isa_pages=isa_pages, save_file=save_file)
        # resul_st_code = self.not_analyze_text(save_file=save_file)

        #         plc_source = """PLC_GP_22_1BR
        # PLC_GP_21_1BR
        # ICore_2
        # GP0016_KTP_SHOL4
        # GP0018_U12
        # GP0016_KTP_SHOL7
        # GP0016_KTP_SHK2
        # GP0016_KTP_SHK8
        # GP018B_KTP_SHOL4
        # GP018B_KTP_SHOL5
        # GP018B_KTP_SHOL6
        # GP018B_KTP_SHOL9
        # GP018B_KTP_SHOL10
        # GP018B_KTP_SHOL11
        # PLC_GP_29_1BR
        # GP018B_KTP_SHOL12
        # PLC_GP_18_1BR
        # ModbusOPCServer
        # GP0022_U4
        # GP018V_KTP_SHOL4
        # GP018V_KTP_SHOL5
        # GP018V_KTP_SHOL6
        # GP018V_KTP_SHOL9
        # GP018V_KTP_SHOL10
        # GP018V_KTP_SHOL11
        # GP018V_KTP_SHOL12
        # PLC_KTP_21
        # GP018A_KTP_SHOL4
        # GP018A_KTP_SHOL5
        # GP018A_KTP_SHOL6
        # GP018A_KTP_SHOL9
        # GP018A_KTP_SHOL10
        # GP018A_KTP_SHOL11
        # GP018A_KTP_SHOL12
        # GP0018_NPORT_U1
        # GP0018_NPORT_U2
        # GP0018_U13
        # GP0018_NPORT_U3
        # GP0018_NPORT_U4
        # GP0018_NPORT_U5
        # GP0018_NPORT_U6
        # GP0021_NPORT_U1
        # GP0021_NPORT_U2
        # GP0021_NPORT_U3
        # GP0021_NPORT_U4
        # GP0021_NPORT_U5
        # GP0021_U10
        # GP0021_U11
        # ASUE_SHS_Huawei_U7
        # ASUE_SHS_Huawei_U8
        # ASUE_SHS_Huawei_S5720_U5
        # GP0029_U2
        # GP0022_U22
        # GP0022_U23
        # GP0015_KOTEL
        # GP0015_REG_3x36
        # GP0022_NPORT_U1
        # GP0022_NPORT_U2
        # GP0022_NPORT_U3
        # GP0022_NPORT_U4
        # GP0022_NPORT_U5
        # GP0022_NPORT_U6
        # GP0022_NPORT_U7
        # GP0022_NPORT_U8
        # GP0022_NPORT_U9
        # GP0022_NPORT_U10
        # GP0022_NPORT_U11
        # GP0022_NPORT_U12
        # GP0022_NPORT_U13
        # GP0022_NPORT_U14
        # GP0022_BR1
        # GP0022_A1
        # GP0022_A2
        # GP0022_A3
        # GP0022_U9
        # GP0022_U10
        # GP0022_A1_IP1
        # GP0022_A1_IP2
        # GP0022_A2_IP1
        # GP0022_A2_IP2
        # GP0022_A3_IP1
        # GP0022_A3_IP2
        # GP0022_U9_IP1
        # GP0022_U9_IP2
        # GP0022_U10_IP1
        # GP0022_U10_IP2
        # GP0029_U6
        # GP0029_U6_IP1
        # PowerOPCServer.DA20
        # PLC_KTP_22""".split('\n')

        plc_source = self.find_plc_source()

        for plc_name in plc_source:

            plc_id = self.find_id_plc(plc_name)

            self.fdb_cur.execute(f"""select MARKA, ID, KLID, OBJTYPEID from CARDS where PLC_ID = {plc_id}""")
            for MARKA, ID, KLID, OBJTYPEID in self.fdb_cur.fetchall():
                type_marka = self.get_type(OBJTYPEID)
                klass_marka = klid.pages_dict_SQL[KLID].NAME
                check_marka = Check_Marka(cursor=self.fdb_cur, marka=MARKA, ID_TO=ID)
                kard = check_marka.find_pages(pages)
                isa_prog = check_marka.find_ISA_pages(isa_pages)
                st_prog = '\n--------\n'.join(resul_st_code.get(ID, ['None']))
                isa = True if check_marka.ID_ISA else False
                self.add_new_row(Marka=MARKA, id_marka=ID, ISA=isa, KLASS=klass_marka, TYPE=type_marka,
                                 PLC_NAME=plc_name,
                                 Pages=kard, ISA_Pages=isa_prog, ST_prog=st_prog)

                self.add_addition_row(id_marka=ID)

        print('Выполнено')

    def get_type(self, OBJTYPEID):
        self.fdb_cur.execute(
            f"select NAME from OBJTYPE where id = {OBJTYPEID}")
        return self.fdb_cur.fetchall()[0][0]

    def find_id_plc(self, plc_name='ICore_2'):
        self.fdb_cur.execute(f"select ID from CARDS where MARKA = '{plc_name}'")
        return self.fdb_cur.fetchall()[0][0]

    def show(self):
        self.cursor.execute("""
                    SELECT 
                        name
                    FROM 
                        sqlite_master 
                    WHERE 
                        type ='table' AND 
                        name NOT LIKE 'sqlite_%';
               		""")

        print(self.cursor.fetchall())

    def add_addition_row(self, id_marka=0):
        self.fdb_cur.execute(
            f"select NAME, DISC, OBJSIGN, OBJNUMBER, PLC_VARNAME, ARH_PER, KKS, OBJDPARAM, SREZCONTROL, EVKLID, PLC_ADRESS, PLC_GR, OBJTYPEID from CARDS where id = {id_marka}")
        NAME, DISC, OBJSIGN, OBJNUMBER, PLC_VARNAME, ARH_PER, KKS, OBJDPARAM, SREZCONTROL, EVKLID, PLC_ADRESS, PLC_GR, OBJTYPEID = \
        self.fdb_cur.fetchall()[0]
        EVGROUP = self.evklid.pages_dict_SQL[EVKLID].NAME
        self.fdb_cur.execute(
            f"select ISAOBJ.NAME from CARDS join   OBJTYPE on CARDS.OBJTYPEID = OBJTYPE.ID join   ISAOBJ on ISAOBJ.ID = OBJTYPE.DEFPOUID where CARDS.ID = {id_marka}")

        TEMPLATE = self.fdb_cur.fetchall()[0][0]
        self.fdb_cur.execute(f"select RESOURCE_NUM from RESOURCES where id = {PLC_GR}")
        try:
            PLC_GROUP = self.fdb_cur.fetchall()[0][0]
        except:
            PLC_GROUP = PLC_GR

        self.cursor.execute(
            f"""INSERT INTO `AdditionalTable`  (id_marka, NAME, DISC, OBJSIGN, OBJNUMBER, PLC_VARNAME, ARH_PER, KKS, OBJDPARAM, SREZCONTROL, EVGROUP, PLC_ADRESS, PLC_GR, TEMPLATE)  VALUES({id_marka}, '{NAME if NAME and NAME != 'None' else ''}', '{DISC if DISC and DISC != 'None' else ''}', '{OBJSIGN if OBJSIGN and OBJSIGN != 'None' else ''}', '{OBJNUMBER if OBJNUMBER and OBJNUMBER != 'None' else ''}', '{PLC_VARNAME if PLC_VARNAME and PLC_VARNAME != 'None' else ''}', '{ARH_PER if ARH_PER and ARH_PER != 'None' else ''}', '{KKS if KKS and KKS != 'None' else ''}', '{OBJDPARAM if OBJDPARAM and OBJDPARAM != 'None' else ''}', '{SREZCONTROL if SREZCONTROL and SREZCONTROL != 'None' else ''}', '{EVGROUP if EVGROUP and EVGROUP != 'None' else ''}', '{PLC_ADRESS if PLC_ADRESS and PLC_ADRESS != 'None' else ''}', '{PLC_GROUP if PLC_GROUP and PLC_GROUP != 'None' else ''}', '{TEMPLATE if TEMPLATE and TEMPLATE != 'None' else ''}');""")
        self.conn.commit()

    def add_new_row(self, id_marka=0, Marka='', ISA=False, KLASS='', TYPE='', PLC_NAME='', Pages='', ISA_Pages='',
                    ST_prog=''):
        self.cursor.execute(
            f"""INSERT INTO `ResultTable`  (id_marka, Marka, KLASS, TYPE, PLC_NAME, ISA, Pages, ISA_Pages, ST_prog)  VALUES({id_marka},'{Marka}', '{KLASS}', '{TYPE}', '{PLC_NAME}', {ISA}, '{Pages}', '{ISA_Pages}', '{ST_prog}');""")
        self.conn.commit()

    def show_table(self):
        self.cursor.execute("""
                    SELECT 
                        *
                    FROM 
                        ResultTable 
               		""")

        print(self.cursor.fetchall())

    def find_plc_source(self, plc_adress=36):
        self.fdb_cur.execute(f"""select MARKA from CARDS where plc_adress = {plc_adress}""")
        return [marka[0] for marka in self.fdb_cur.fetchall()]

# if __name__ == '__main__':
#     new_BD = DB_Result()
#     new_BD.firebird_db_init(path_db)
