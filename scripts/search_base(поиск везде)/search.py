# -*- coding: utf-8 -*-
import fdb

con = fdb.connect(dsn="C:\\Users\\Gazauto\\Downloads\\test\\SCADABD.GDB", user='sysdba', password='masterkey', charset='utf8')
cur = con.cursor()

SELECT = """select rdb$relation_name 
from rdb$relation_fields 
where rdb$field_name  = 'NAME'"""
cur.execute(SELECT)

list_ = []
for Name in cur:
    name_nw = str(Name[0]).split()[0]

    list_.append(name_nw)

for i, el in enumerate(list_):
    print(i, '-', el)

for inde, table in enumerate(list_):
    SELECT = f"""select ID from {table}  where NAME = 'FB_VentControlWithOrder'"""
    try:
        cur.execute(SELECT)
        all = cur.fetchall()
        if len(all) != 0:
            print(all, sep='-')
            print(inde, end='\n')
    except:
        pass
