import re

com_ports = """mb_master_hr_int_v	[COM1013:1:130]	3
mb_master_hr_int_v	[COM1013:1:36]	10
mb_master_hr_real_v	[COM1013:1:32]	1
mb_master_hr_int_v	[COM1013:1:151]	3
mb_master_hr_real_v	[COM1013:1:147]	1
mb_master_hr_int_v	[COM1013:1:1]	4
mb_master_hr_int_v	[COM1013:1:31]	1
mb_master_hr_real_v	[COM1013:1:5]	11
mb_master_hr_int_v	[COM1013:1:154]	4
mb_master_hr_real_v	[COM1013:1:158]	11
mb_master_hr_int_v	[COM1013:1:180]	1
mb_master_hr_real_v	[COM1013:1:181]	14
mb_master_hr_int_v	[COM1013:1:216]	15
mb_master_hr_int_v	[COM1013:1:270]	1
mb_master_hr_real_v	[COM1013:1:264]	3
mb_master_hr_real_v	[COM1013:1:271]	14
mb_master_hr_int_v	[COM1013:1:306]	15
mb_master_hr_int_v	[COM1013:1:347]	1
mb_master_hr_real_v	[COM1013:1:341]	3
mb_master_hr_int_v	[COM1013:1:133]	2
mb_master_hr_real_v	[COM1013:1:135]	1
mb_master_hr_real_v	[COM1013:1:139]	1
mb_master_hr_real_v	[COM1013:1:143]	1""".split('\n')
dict_1 = {
    'mb_master_hr_int_v': '.ValueDINT',
    'mb_master_hr_real_v': '.ValueREAL'
}

data_Info = {}


class Info:
    def __init__(self, reg, com, com_start, com_end, data,count):
        self.reg = reg
        self.com = com
        self.com_start = com_start
        self.com_end = com_end
        self.data = data
        self.count =count


for com_port in com_ports:
    reg, com, count = com_port.split('\t')
    com_start = int(com.split(':')[2][0:-1])

    if reg == 'mb_master_hr_real_v':
        com_end = com_start + int(count)*2 - 1
    else:
        com_end = com_start + int(count) - 1
    data_Info.update({f'{com_start}:{com_end}': Info(reg, com, com_start, com_end, dict_1.get(reg),count)})

excel_data = """GP0022_SHPT1_SHPN3_BYPASS_PARALLEL_MS	ШПН3. Режим параллельной работы байпаса=0:Ведущий	231	BOOL
GP0022_SHPT1_SHPN3_BYPASS_PARALLEL_MS_fromINV	ШПН3. Режим параллельной работы байпаса=1:Ведущий-от Инвертора	231	BOOL
GP0022_SHPT1_SHPN3_BYPASS_PARALLEL_MS_fromRSEE	ШПН3. Режим параллельной работы байпаса=2:Ведущий-от РСЭЭ	231	BOOL
GP0022_SHPT1_SHPN3_BYPASS_PARALLEL_SL	ШПН3. Режим параллельной работы байпаса=3:Ведомый	231	BOOL
GP0022_SHPT1_SHPN3_BYPASS_PARALLEL_READY	ШНП3. Режим параллельной работы байпаса=4:Готовность	231	BOOL
GP0022_SHPT1_SHPN3_INV_READY	ШПН3. INV: Состояние =0: Готовность	244	BOOL
GP0022_SHPT1_SHPN3_INV_SOFTSTART	ШПН3. INV: Состояние =1: Мягкий старт	244	BOOL
GP0022_SHPT1_SHPN3_INV_SOFTSTART2	ШПН3. INV: Состояние =2: Мягкий старт 2	244	BOOL
GP0022_SHPT1_SHPN3_INV_ON	ШПН3. INV: Состояние =3: ВКЛЮЧЕНИЕ	244	BOOL
GP0022_SHPT1_SHPN3_INV_WORK	ШПН3. INV: Состояние =4: Работа	244	BOOL
GP0022_SHPT1_SHPN3_INV_OFF	ШПН3. INV: Состояние =5: ОТКЛЮЧЕНИЕ	244	BOOL
GP0022_SHPT1_SHPN3_INV_FAULT_WORK	ШПН3. INV: Состояние =6: Ошибка работы	244	BOOL
GP0022_SHPT1_SHPN3_INVstat_OK	ШПН3. INV: Статус =0: OK	245	BOOL
GP0022_SHPT1_SHPN3_INVstat_ALARM	ШПН3. INV: Статус =1: Тревога	245	BOOL
GP0022_SHPT1_SHPN3_INVstat_WARNING	ШПН3. INV: Статус =2: Предупреждение 	245	BOOL
GP0022_SHPT1_SHPN3_INVmode_MS	ШПН3. INV: Режим работы =0: Ведущий	246	BOOL
GP0022_SHPT1_SHPN3_INVmode_SL	ШПН3. INV: Режим работы =1: Ведомый	246	BOOL
GP0022_SHPT1_SHPN3_INVmode_READY	ШПН3. INV: Режим работы =2: Готовность	246	BOOL
GP0022_SHPT1_SHPN4_BYPASS_PARALLEL_MS	ШПН4. Режим параллельной работы байпаса=0:Ведущий	321	BOOL
GP0022_SHPT1_SHPN4_BYPASS_PARALLEL_MS_fromINV	ШПН4. Режим параллельной работы байпаса=1:Ведущий-от Инвертора	321	BOOL
GP0022_SHPT1_SHPN4_BYPASS_PARALLEL_MS_fromRSEE	ШПН4. Режим параллельной работы байпаса=2:Ведущий-от РСЭЭ	321	BOOL
GP0022_SHPT1_SHPN4_BYPASS_PARALLEL_SL	ШПН4. Режим параллельной работы байпаса=3:Ведомый	321	BOOL
GP0022_SHPT1_SHPN4_BYPASS_PARALLEL_READY	ШНП3. Режим параллельной работы байпаса=4:Готовность	321	BOOL
GP0022_SHPT1_SHPN4_INV_READY	ШПН4. INV: Состояние =0: Готовность	334	BOOL
GP0022_SHPT1_SHPN4_INV_SOFTSTART	ШПН4. INV: Состояние =1: Мягкий старт	334	BOOL
GP0022_SHPT1_SHPN4_INV_SOFTSTART2	ШПН4. INV: Состояние =2: Мягкий старт 2	334	BOOL
GP0022_SHPT1_SHPN4_INV_ON	ШПН4. INV: Состояние =3: ВКЛЮЧЕНИЕ	334	BOOL
GP0022_SHPT1_SHPN4_INV_WORK	ШПН4. INV: Состояние =4: Работа	334	BOOL
GP0022_SHPT1_SHPN4_INV_OFF	ШПН4. INV: Состояние =5: ОТКЛЮЧЕНИЕ	334	BOOL
GP0022_SHPT1_SHPN4_INV_FAULT_WORK	ШПН4. INV: Состояние =6: Ошибка работы	334	BOOL
GP0022_SHPT1_SHPN4_INVstat_OK	ШПН4. INV: Статус =0: OK	335	BOOL
GP0022_SHPT1_SHPN4_INVstat_ALARM	ШПН4. INV: Статус =1: Тревога	335	BOOL
GP0022_SHPT1_SHPN4_INVstat_WARNING	ШПН4. INV: Статус =2: Предупреждение 	335	BOOL
GP0022_SHPT1_SHPN4_INVmode_MS	ШПН4. INV: Режим работы =0: Ведущий	336	BOOL
GP0022_SHPT1_SHPN4_INVmode_SL	ШПН4. INV: Режим работы =1: Ведомый	336	BOOL
GP0022_SHPT1_SHPN4_INVmode_READY	ШПН4. INV: Режим работы =2: Готовность	336	BOOL""".split('\n')


def find_Info(reg):
    for key_d in data_Info.keys():
        com_start, com_end = map(int, key_d.split(':'))
        if reg >= com_start and reg <= com_end:
            return data_Info[key_d]

def find_num(desc):
    result = re.findall(r'=[0-9]+\:',desc)

    return result[0][1:-1]
list_err=[]
# int to BOOL
for data_exc in excel_data:
    marka, desc, adress, type_data = data_exc.split('\t')
    # if type_data != 'INT':
    #     continue
    num =find_num(desc)
    registr = adress
    info_reg = find_Info(int(registr))
    if info_reg:
        print(f'''(*{desc}*)
{marka}.In := <<{info_reg.com} mb_master_hr_int_in_v > канал {int(registr)-info_reg.com_start}>>.ValueDINT = {num}; (*REG={adress}/{info_reg.com}*)
{marka}.Invalid :=  FC_StatusDI(<<{info_reg.com} mb_master_hr_int_in_v > канал {int(registr)-info_reg.com_start}>>.Status);
''')
    else:
        list_err.append(f'{data_exc}')

print('\n'.join(list_err))
list_err = []
# BOOL
# for data_exc in excel_data:
#     marka, desc, adress, type_data = data_exc.split('\t')
#     if type_data != 'BOOL':
#         continue
#
#     registr, bit = adress.split('.')
#     info_reg = find_Info(int(registr))
#     if info_reg:
#         print(f'''(*{desc}*)
# {marka}.In := BITGET(<<{info_reg.com} mb_master_hr_int_in_v > канал {int(registr)-info_reg.com_start}>>.ValueDINT, {bit}); (*REG={adress}/{info_reg.com}*)
# {marka}.Invalid :=  FC_StatusDI(<<{info_reg.com} mb_master_hr_int_in_v > канал {int(registr)-info_reg.com_start}>>.Status);
# ''')
#     else:
#         list_err.append(f'{data_exc}')

list_as=[]
# real
# for data_exc in excel_data:
#     marka, desc, adress, type_data = data_exc.split('\t')
#     if type_data != 'REAL':
#         continue
#
#     registr = adress
#     info_reg = find_Info(int(registr))
#     if info_reg:
#         print(f'''(*{desc}*)
# {marka}.In := <<{info_reg.com} mb_master_hr_real_in_v > канал {(int(registr)-info_reg.com_start)//2}>>.ValueREAL; (*REG={adress}/{info_reg.com}*)
# {marka}.Invalid :=  FC_StatusAI(<<{info_reg.com} mb_master_hr_real_in_v > канал {(int(registr)-info_reg.com_start)//2}>>.Status);
# ''')
#         list_as.append(f'{data_exc}')
#     else:
#         list_err.append(f'{data_exc}')
#
# print('\n'.join(list_as))
# int to real
# for data_exc in excel_data:
#     marka, desc, adress, type_data = data_exc.split('\t')
#     if type_data != 'INT':
#         continue
#
#     registr = adress
#     info_reg = find_Info(int(registr))
#     if info_reg:
#         print(f'''(*{desc}*)
# {marka}.In := ANY_TO_REAL(<<{info_reg.com} mb_master_hr_int_in_v > канал {int(registr)-info_reg.com_start}>>.ValueDINT); (*REG={adress}/{info_reg.com}*)
# {marka}.Invalid :=  FC_StatusDI(<<{info_reg.com} mb_master_hr_int_in_v > канал {int(registr)-info_reg.com_start}>>.Status);
# ''')
#     else:
#         list_err.append(f'{data_exc}')

data_qf = """GP0022_SHPT1_QF1.InOff	ШОЛ1. QF1 Отключен	130.0	BOOL
GP0022_SHPT1_QF1.InOn	ШОЛ1. QF1 Включен	130.1	BOOL
GP0022_SHPT1_QF2.InOff	ШОЛ1. QF2 Отключен	130.2	BOOL
GP0022_SHPT1_QF2.InOn	ШОЛ1. QF2 Включен	130.3	BOOL
GP0022_SHPT1_QF3.InOff	ШОЛ1. QF3 Отключен	130.4	BOOL
GP0022_SHPT1_QF3.InOn	ШОЛ1. QF3 Включен	130.5	BOOL
GP0022_SHPT1_QF4.InOff	ШОЛ1. QF4 Отключен	130.6	BOOL
GP0022_SHPT1_QF4.InOn	ШОЛ1. QF4 Включен	130.7	BOOL
GP0022_SHPT1_QF5.InOff	ШОЛ1. QF5 Отключен	130.8	BOOL
GP0022_SHPT1_QF5.InOn	ШОЛ1. QF5 Включен	130.9	BOOL
GP0022_SHPT1_QF6.InOff	ШОЛ1. QF6 Отключен	130.10	BOOL
GP0022_SHPT1_QF6.InOn	ШОЛ1. QF6 Включен	130.11	BOOL
GP0022_SHPT1_QF7.InOff	ШОЛ1. QF7 Отключен	130.12	BOOL
GP0022_SHPT1_QF7.InOn	ШОЛ1. QF7 Включен	130.13	BOOL
GP0022_SHPT1_QF8.InOff	ШОЛ1. QF8 Отключен	130.14	BOOL
GP0022_SHPT1_QF8.InOn	ШОЛ1. QF8 Включен	130.15	BOOL
GP0022_SHPT1_QF9.InOff	ШОЛ1. QF9 Отключен	131.0	BOOL
GP0022_SHPT1_QF9.InOn	ШОЛ1. QF9 Включен	131.1	BOOL
GP0022_SHPT1_QF10.InOff	ШОЛ1. QF10 Отключен	131.2	BOOL
GP0022_SHPT1_QF10.InOn	ШОЛ1. QF10 Включен	131.3	BOOL
GP0022_SHPT1_QF11.InOff	ШОЛ1. QF11 Отключен	131.4	BOOL
GP0022_SHPT1_QF11.InOn	ШОЛ1. QF11 Включен	131.5	BOOL
GP0022_SHPT1_QF12.InOff	ШОЛ1. QF12 Отключен	131.6	BOOL
GP0022_SHPT1_QF12.InOn	ШОЛ1. QF12 Включен	131.7	BOOL
GP0022_SHPT1_QF13.InOff	ШОЛ1. QF13 Отключен	131.8	BOOL
GP0022_SHPT1_QF13.InOn	ШОЛ1. QF13 Включен	131.9	BOOL
GP0022_SHPT1_QF14.InOff	ШОЛ1. QF14 Отключен	131.10	BOOL
GP0022_SHPT1_QF14.InOn	ШОЛ1. QF14 Включен	131.11	BOOL
GP0022_SHPT1_QF15.InOff	ШОЛ1. QF15 Отключен	132.0	BOOL
GP0022_SHPT1_QF15.InOn	ШОЛ1. QF15 Включен	132.1	BOOL
GP0022_SHPT1_QF16.InOff	ШОЛ1. QF16 Отключен	132.2	BOOL
GP0022_SHPT1_QF16.InOn	ШОЛ1. QF16 Включен	132.3	BOOL
GP0022_SHPT1_QF17.InOff	ШОЛ1. QF17 Отключен	132.4	BOOL
GP0022_SHPT1_QF17.InOn	ШОЛ1. QF17 Включен	132.5	BOOL
GP0022_SHPT1_QF18.InOff	ШОЛ1. QF18 Отключен	132.6	BOOL
GP0022_SHPT1_QF18.InOn	ШОЛ1. QF18 Включен	132.7	BOOL
GP0022_SHPT1_QF19.InOff	ШОЛ1. QF19 Отключен	132.8	BOOL
GP0022_SHPT1_QF19.InOn	ШОЛ1. QF19 Включен	132.9	BOOL
GP0022_SHPT1_QF20.InOff	ШОЛ1. QF20 Отключен	132.10	BOOL
GP0022_SHPT1_QF20.InOn	ШОЛ1. QF20 Включен	132.11	BOOL
GP0022_SHPT1_QF21.InOff	ШОЛ1. QF21 Отключен	132.12	BOOL
GP0022_SHPT1_QF21.InOn	ШОЛ1. QF21 Включен	132.13	BOOL
GP0022_SHPT1_QF1.InEOff	ШОЛ1. QF1 Аварийное срабатывание защитного аппарата	132.14	BOOL
GP0022_SHPT1_QF2.InEOff	ШОЛ1. QF2 Аварийное срабатывание защитного аппарата	132.14	BOOL
GP0022_SHPT1_QF3.InEOff	ШОЛ1. QF3 Аварийное срабатывание защитного аппарата	132.14	BOOL
GP0022_SHPT1_QF4.InEOff	ШОЛ1. QF4 Аварийное срабатывание защитного аппарата	132.14	BOOL
GP0022_SHPT1_QF5.InEOff	ШОЛ1. QF5 Аварийное срабатывание защитного аппарата	132.14	BOOL
GP0022_SHPT1_QF6.InEOff	ШОЛ1. QF6 Аварийное срабатывание защитного аппарата	132.14	BOOL
GP0022_SHPT1_QF7.InEOff	ШОЛ1. QF7 Аварийное срабатывание защитного аппарата	132.14	BOOL
GP0022_SHPT1_QF8.InEOff	ШОЛ1. QF8 Аварийное срабатывание защитного аппарата	132.14	BOOL
GP0022_SHPT1_QF9.InEOff	ШОЛ1. QF9 Аварийное срабатывание защитного аппарата	132.14	BOOL
GP0022_SHPT1_QF10.InEOff	ШОЛ1. QF10 Аварийное срабатывание защитного аппарата	132.14	BOOL
GP0022_SHPT1_QF11.InEOff	ШОЛ1. QF11 Аварийное срабатывание защитного аппарата	132.14	BOOL
GP0022_SHPT1_QF12.InEOff	ШОЛ1. QF12 Аварийное срабатывание защитного аппарата	132.14	BOOL
GP0022_SHPT1_QF13.InEOff	ШОЛ1. QF13 Аварийное срабатывание защитного аппарата	132.14	BOOL
GP0022_SHPT1_QF14.InEOff	ШОЛ1. QF14 Аварийное срабатывание защитного аппарата	132.14	BOOL
GP0022_SHPT1_QF15.InEOff	ШОЛ1. QF15 Аварийное срабатывание защитного аппарата	132.14	BOOL
GP0022_SHPT1_QF16.InEOff	ШОЛ1. QF16 Аварийное срабатывание защитного аппарата	132.14	BOOL
GP0022_SHPT1_QF17.InEOff	ШОЛ1. QF17 Аварийное срабатывание защитного аппарата	132.14	BOOL
GP0022_SHPT1_QF18.InEOff	ШОЛ1. QF18 Аварийное срабатывание защитного аппарата	132.14	BOOL
GP0022_SHPT1_QF19.InEOff	ШОЛ1. QF19 Аварийное срабатывание защитного аппарата	132.14	BOOL
GP0022_SHPT1_QF20.InEOff	ШОЛ1. QF20 Аварийное срабатывание защитного аппарата	132.14	BOOL
GP0022_SHPT1_QF21.InEOff	ШОЛ1. QF21 Аварийное срабатывание защитного аппарата	132.14	BOOL
GP0022_SHPT1_QS1.InOff	ШОЛ1. QS1 Отключен	132.15	BOOL
GP0022_SHPT1_QS1.InOn	ШОЛ1. QS1 Включен	132.15	BOOL
GP0022_SHPT1_2QF.InOff	ШВВ. 2QF Отключен	133.0	BOOL
GP0022_SHPT1_2QF.InOn	ШВВ. 2QF Включен	133.1	BOOL
GP0022_SHPT1_2QF.InEOff	ШВВ. 2QF Аварийное отключение	133.2	BOOL
GP0022_SHPT1_6QF.InOff	ШВВ. 6QF Отключен	133.3	BOOL
GP0022_SHPT1_6QF.InOn	ШВВ. 6QF Включен	133.4	BOOL
GP0022_SHPT1_6QF.InEOff	ШВВ. 6QF Аварийное отключение	133.5	BOOL
GP0022_SHPT1_8QF.InOff	ШВВ. 8QF Отключен	133.6	BOOL
GP0022_SHPT1_8QF.InOn	ШВВ. 8QF Включен	133.7	BOOL
GP0022_SHPT1_8QF.InEOff	ШВВ. 8QF Аварийное отключение	133.8	BOOL
GP0022_SHPT1_3QF.InOff	ШВВ. 3QF Отключен	134.0	BOOL
GP0022_SHPT1_3QF.InOn	ШВВ. 3QF Включен	134.1	BOOL
GP0022_SHPT1_4QF.InOff	ШВВ. 4QF Отключен	134.2	BOOL
GP0022_SHPT1_4QF.InOn	ШВВ. 4QF Включен	134.3	BOOL
GP0022_SHPT1_4QF.InEOff	ШВВ. 4QF Аварийное отключение	134.4	BOOL
GP0022_SHPT1_1QF.InOff	ШВВ. 1QF Отключен	134.5	BOOL
GP0022_SHPT1_1QF.InOn	ШВВ. 1QF Включен	134.6	BOOL
GP0022_SHPT1_1QF.InEOff	ШВВ. 1QF Аварийное отключение	134.7	BOOL
GP0022_SHPT1_5QF.InOff	ШВВ. 5QF Отключен	134.8	BOOL
GP0022_SHPT1_5QF.InOn	ШВВ. 5QF Включен	134.9	BOOL
GP0022_SHPT1_5QF.InEOff	ШВВ. 5QF Аварийное отключение	134.10	BOOL
GP0022_SHPT1_7QF.InOff	ШВВ. 7QF Отключен	134.11	BOOL
GP0022_SHPT1_7QF.InOn	ШВВ. 7QF Включен	134.12	BOOL
GP0022_SHPT1_7QF.InEOff	ШВВ. 7QF Аварийное отключение	134.13	BOOL
GP0022_SHPT1_QF22.InOff	ШОЛ2. QF22 Отключен	151.0	BOOL
GP0022_SHPT1_QF22.InOn	ШОЛ2. QF22 Включен	151.1	BOOL
GP0022_SHPT1_QF23.InOff	ШОЛ2. QF23 Отключен	151.2	BOOL
GP0022_SHPT1_QF23.InOn	ШОЛ2. QF23 Включен	151.3	BOOL
GP0022_SHPT1_QF24.InOff	ШОЛ2. QF24 Отключен	151.4	BOOL
GP0022_SHPT1_QF24.InOn	ШОЛ2. QF24 Включен	151.5	BOOL
GP0022_SHPT1_QF25.InOff	ШОЛ2. QF25 Отключен	151.6	BOOL
GP0022_SHPT1_QF25.InOn	ШОЛ2. QF25 Включен	151.7	BOOL
GP0022_SHPT1_QF26.InOff	ШОЛ2. QF26 Отключен	151.8	BOOL
GP0022_SHPT1_QF26.InOn	ШОЛ2. QF26 Включен	151.9	BOOL
GP0022_SHPT1_QF27.InOff	ШОЛ2. QF27 Отключен	151.10	BOOL
GP0022_SHPT1_QF27.InOn	ШОЛ2. QF27 Включен	151.11	BOOL
GP0022_SHPT1_QF28.InOff	ШОЛ2. QF28 Отключен	151.12	BOOL
GP0022_SHPT1_QF28.InOn	ШОЛ2. QF28 Включен	151.13	BOOL
GP0022_SHPT1_QF29.InOff	ШОЛ2. QF29 Отключен	151.14	BOOL
GP0022_SHPT1_QF29.InOn	ШОЛ2. QF29 Включен	151.15	BOOL
GP0022_SHPT1_QF30.InOff	ШОЛ2. QF30 Отключен	152.0	BOOL
GP0022_SHPT1_QF30.InOn	ШОЛ2. QF30 Включен	152.1	BOOL
GP0022_SHPT1_QF31.InOff	ШОЛ2. QF31 Отключен	152.2	BOOL
GP0022_SHPT1_QF31.InOn	ШОЛ2. QF31 Включен	152.3	BOOL
GP0022_SHPT1_QF32.InOff	ШОЛ2. QF32 Отключен	152.4	BOOL
GP0022_SHPT1_QF32.InOn	ШОЛ2. QF32 Включен	152.5	BOOL
GP0022_SHPT1_QF33.InOff	ШОЛ2. QF33 Отключен	152.6	BOOL
GP0022_SHPT1_QF33.InOn	ШОЛ2. QF33 Включен	152.7	BOOL
GP0022_SHPT1_QF34.InOff	ШОЛ2. QF34 Отключен	152.8	BOOL
GP0022_SHPT1_QF34.InOn	ШОЛ2. QF34 Включен	152.9	BOOL
GP0022_SHPT1_QF35.InOff	ШОЛ2. QF35 Отключен	152.10	BOOL
GP0022_SHPT1_QF35.InOn	ШОЛ2. QF35 Включен	152.11	BOOL
GP0022_SHPT1_QF36.InOff	ШОЛ2. QF36 Отключен	153.0	BOOL
GP0022_SHPT1_QF36.InOn	ШОЛ2. QF36 Включен	153.1	BOOL
GP0022_SHPT1_QF37.InOff	ШОЛ2. QF37 Отключен	153.2	BOOL
GP0022_SHPT1_QF37.InOn	ШОЛ2. QF37 Включен	153.3	BOOL
GP0022_SHPT1_QF38.InOff	ШОЛ2. QF38 Отключен	153.4	BOOL
GP0022_SHPT1_QF38.InOn	ШОЛ2. QF38 Включен	153.5	BOOL
GP0022_SHPT1_QF39.InOff	ШОЛ2. QF39 Отключен	153.6	BOOL
GP0022_SHPT1_QF39.InOn	ШОЛ2. QF39 Включен	153.7	BOOL
GP0022_SHPT1_QF40.InOff	ШОЛ2. QF40 Отключен	153.8	BOOL
GP0022_SHPT1_QF40.InOn	ШОЛ2. QF40 Включен	153.9	BOOL
GP0022_SHPT1_QF41.InOff	ШОЛ2. QF41 Отключен	153.10	BOOL
GP0022_SHPT1_QF41.InOn	ШОЛ2. QF41 Включен	153.11	BOOL
GP0022_SHPT1_QF42.InOff	ШОЛ2. QF42 Отключен	153.12	BOOL
GP0022_SHPT1_QF42.InOn	ШОЛ2. QF42 Включен	153.13	BOOL
GP0022_SHPT1_QF22.InEOff	ШОЛ1. QF22 Аварийное срабатывание защитного аппарата	153.14	BOOL
GP0022_SHPT1_QF23.InEOff	ШОЛ1. QF23 Аварийное срабатывание защитного аппарата	153.14	BOOL
GP0022_SHPT1_QF24.InEOff	ШОЛ1. QF24 Аварийное срабатывание защитного аппарата	153.14	BOOL
GP0022_SHPT1_QF25.InEOff	ШОЛ1. QF25 Аварийное срабатывание защитного аппарата	153.14	BOOL
GP0022_SHPT1_QF26.InEOff	ШОЛ1. QF26 Аварийное срабатывание защитного аппарата	153.14	BOOL
GP0022_SHPT1_QF27.InEOff	ШОЛ1. QF27 Аварийное срабатывание защитного аппарата	153.14	BOOL
GP0022_SHPT1_QF28.InEOff	ШОЛ1. QF28 Аварийное срабатывание защитного аппарата	153.14	BOOL
GP0022_SHPT1_QF29.InEOff	ШОЛ1. QF29 Аварийное срабатывание защитного аппарата	153.14	BOOL
GP0022_SHPT1_QF30.InEOff	ШОЛ1. QF30 Аварийное срабатывание защитного аппарата	153.14	BOOL
GP0022_SHPT1_QF31.InEOff	ШОЛ1. QF31 Аварийное срабатывание защитного аппарата	153.14	BOOL
GP0022_SHPT1_QF32.InEOff	ШОЛ1. QF32 Аварийное срабатывание защитного аппарата	153.14	BOOL
GP0022_SHPT1_QF33.InEOff	ШОЛ1. QF33 Аварийное срабатывание защитного аппарата	153.14	BOOL
GP0022_SHPT1_QF34.InEOff	ШОЛ1. QF34 Аварийное срабатывание защитного аппарата	153.14	BOOL
GP0022_SHPT1_QF35.InEOff	ШОЛ1. QF35 Аварийное срабатывание защитного аппарата	153.14	BOOL
GP0022_SHPT1_QF36.InEOff	ШОЛ1. QF36 Аварийное срабатывание защитного аппарата	153.14	BOOL
GP0022_SHPT1_QF37.InEOff	ШОЛ1. QF37 Аварийное срабатывание защитного аппарата	153.14	BOOL
GP0022_SHPT1_QF38.InEOff	ШОЛ1. QF38 Аварийное срабатывание защитного аппарата	153.14	BOOL
GP0022_SHPT1_QF39.InEOff	ШОЛ1. QF39 Аварийное срабатывание защитного аппарата	153.14	BOOL
GP0022_SHPT1_QF40.InEOff	ШОЛ1. QF40 Аварийное срабатывание защитного аппарата	153.14	BOOL
GP0022_SHPT1_QF41.InEOff	ШОЛ1. QF41 Аварийное срабатывание защитного аппарата	153.14	BOOL
GP0022_SHPT1_QF42.InEOff	ШОЛ1. QF42 Аварийное срабатывание защитного аппарата	153.14	BOOL
GP0022_SHPT1_QS2.InOff	ШОЛ2. QS2 Отключен	153.15	BOOL
GP0022_SHPT1_QS2.InOn	ШОЛ2. QS2 Включен	153.15	BOOL
GP0022_SHPT1_1QF1.InOff	ШПН3. 1QF1 Отключен	270.0	BOOL
GP0022_SHPT1_1QF1.InOn	ШПН3. 1QF1 Включен	270.1	BOOL
GP0022_SHPT1_1QF1.InEOff	ШПН3. 1QF1 Аварийное отключение	270.2	BOOL
GP0022_SHPT1_1QF2.InOff	ШПН3. 1QF2 Отключен	270.3	BOOL
GP0022_SHPT1_1QF2.InOn	ШПН3. 1QF2 Включен	270.4	BOOL
GP0022_SHPT1_1QF2.InEOff	ШПН3. 1QF2 Аварийное отключение	270.5	BOOL
GP0022_SHPT1_1QF3.InOff	ШПН3. 1QF3 Отключен	270.6	BOOL
GP0022_SHPT1_1QF3.InOn	ШПН3. 1QF3 Включен	270.7	BOOL
GP0022_SHPT1_1QF3.InEOff	ШПН3. 1QF3 Аварийное отключение	270.8	BOOL
GP0022_SHPT1_1QW1.InOff	ШПН3. 1QW1 Отключен	270.9	BOOL
GP0022_SHPT1_1QW1.InOn	ШПН3. 1QW1 Включен	270.9	BOOL
GP0022_SHPT1_1QW2.InOff	ШПН3. 1QW2 Отключен	270.10	BOOL
GP0022_SHPT1_1QW2.InOn	ШПН3. 1QW2 Включен	270.10	BOOL
GP0022_SHPT1_1QW3.InOff	ШПН3. 1QW3 Отключен	270.11	BOOL
GP0022_SHPT1_1QW3.InOn	ШПН3. 1QW3 Включен	270.11	BOOL
GP0022_SHPT1_1QW4.InOff	ШПН3. 1QW4 Отключен	270.12	BOOL
GP0022_SHPT1_1QW5.InOn	ШПН3. 1QW5 Отключен	270.13	BOOL
GP0022_SHPT1_1QW4.InOff	ШПН3. 1QW4 Включен	270.14	BOOL
GP0022_SHPT1_1QW5.InOn	ШПН3. 1QW5 Включен	270.15	BOOL
GP0022_SHPT1_2QF1.InOff	ШПН4. 2QF1 Отключен	347.0	BOOL
GP0022_SHPT1_2QF1.InOn	ШПН4. 2QF1 Включен	347.1	BOOL
GP0022_SHPT1_2QF1.InEOff	ШПН4. 2QF1 Аварийное отключение	347.2	BOOL
GP0022_SHPT1_2QF2.InOff	ШПН4. 2QF2 Отключен	347.3	BOOL
GP0022_SHPT1_2QF2.InOn	ШПН4. 2QF2 Включен	347.4	BOOL
GP0022_SHPT1_2QF2.InEOff	ШПН4. 2QF2 Аварийное отключение	347.5	BOOL
GP0022_SHPT1_2QF3.InOff	ШПН4. 2QF3 Отключен	347.6	BOOL
GP0022_SHPT1_2QF3.InOn	ШПН4. 2QF3 Включен	347.7	BOOL
GP0022_SHPT1_2QF3.InEOff	ШПН4. 2QF3 Аварийное отключение	347.8	BOOL
GP0022_SHPT1_2QW1.InOff	ШПН4. 2QW1 Отключен	347.9	BOOL
GP0022_SHPT1_2QW1.InOn	ШПН4. 2QW1 Включен	347.9	BOOL
GP0022_SHPT1_2QW2.InOff	ШПН4. 2QW2 Отключен	347.10	BOOL
GP0022_SHPT1_2QW2.InOn	ШПН4. 2QW2 Включен	347.10	BOOL
GP0022_SHPT1_2QW3.InOff	ШПН4. 2QW3 Отключен	347.11	BOOL
GP0022_SHPT1_2QW3.InOn	ШПН4. 2QW3 Включен	347.11	BOOL
GP0022_SHPT1_2QW4.InOff	ШПН4. 2QW4 Отключен	347.12	BOOL
GP0022_SHPT1_2QW5.InOn	ШПН4. 2QW5 Отключен	347.13	BOOL
GP0022_SHPT1_2QW4.InOff	ШПН4. 2QW4 Включен	347.14	BOOL
GP0022_SHPT1_2QW5.InOn	ШПН4. 2QW5 Включен	347.15	BOOL""".split('\n')

def get_invalid(end):
    if end == 'InOn':
        return 'InvalidOn'
    elif end =='InOff':
        return 'InvalidOff'
    return 'InvalidEOff'


# QF
# for data_exc in data_qf:
#     marka, desc, adress, type_data = data_exc.split('\t')
#     # if type_data != 'INT':
#     #     continue
#
#     registr, bit = adress.split('.')
#     info_reg = find_Info(int(registr))
#     marka_invalid = f"{marka.split('.')[0]}.{get_invalid(marka.split('.')[1])}"
#
#
#     if info_reg:
#         print(f'''{marka} := BITGET(<<{info_reg.com} mb_master_hr_int_in_v > канал {int(registr)-info_reg.com_start}>>.ValueDINT, {bit});(*{desc}*) (*REG={adress}/{info_reg.com}*)
# {marka_invalid} := FC_StatusDI(<<{info_reg.com} mb_master_hr_int_in_v > канал {int(registr) - info_reg.com_start}>>.ValueDINT);(*{desc}*) (*REG={adress}/{info_reg.com}*)
# ''')
#
#     else:
#         list_err.append(f'{data_exc}')

# real
'''GP0011_PE1_P.In := <<[COM1023:1:108] mb_master_hr_real_out_v > канал 0>>.ValueREAL;
GP0011_PE1_P.Invalid :=FC_StatusAI(_IO_IX18_0_0.Status);'''

# bool
'''GP0021_SEO1_2_TH15.In := BITGET(_IO_IX40_0_0.ValueDINT, 0);
GP0021_SEO1_2_TH15.Invalid :=  FC_StatusDI(_IO_IX40_0_0.Status);'''

# int
'''GP0021_SEO2_ES_1_I67_1.In := REAL_TO_DINT(_IO_IX46_1_0.ValueDINT);
GP0021_SEO2_ES_1_I67_1.Invalid := FC_StatusAI(_IO_IX46_1_0.Status);'''


print('\n'.join(list_err))