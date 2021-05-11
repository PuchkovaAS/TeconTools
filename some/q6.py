code = """GP0022_SHPT2_5QF.InOff := BITGET(_IO_IX50_0_0.ValueDINT, 0);(*ШВВ. 5QF Отключен*) (*REG=98.0/[COM1023:1:98]*)
GP0022_SHPT2_5QF.InOn := BITGET(_IO_IX50_0_0.ValueDINT, 1);(*ШВВ. 5QF Включен*) (*REG=98.1/[COM1023:1:98]*)

GP0022_SHPT2_6QF.InOff := BITGET(_IO_IX50_0_0.ValueDINT, 2);(*ШВВ. 6QF Отключен*) (*REG=98.2/[COM1023:1:98]*)
GP0022_SHPT2_6QF.InOn := BITGET(_IO_IX50_0_0.ValueDINT, 3);(*ШВВ. 6QF Включен*) (*REG=98.3/[COM1023:1:98]*)
GP0022_SHPT2_6QF.InEOff := BITGET(_IO_IX50_0_0.ValueDINT, 4);(*ШВВ. 6QF Аварийное отключение*) (*REG=98.4/[COM1023:1:98]*)

GP0022_SHPT2_1QF.InOff := BITGET(_IO_IX50_0_0.ValueDINT, 5);(*ШВВ. 1QF Отключен*) (*REG=98.5/[COM1023:1:98]*)
GP0022_SHPT2_1QF.InOn := BITGET(_IO_IX50_0_0.ValueDINT, 6);(*ШВВ. 1QF Включен*) (*REG=98.6/[COM1023:1:98]*)
GP0022_SHPT2_1QF.InEOff := BITGET(_IO_IX50_0_0.ValueDINT, 7);(*ШВВ. 1QF Аварийное отключение*) (*REG=98.7/[COM1023:1:98]*)

GP0022_SHPT2_3QF.InOff := BITGET(_IO_IX50_0_0.ValueDINT, 8);(*ШВВ. 3QF Отключен*) (*REG=98.8/[COM1023:1:98]*)
GP0022_SHPT2_3QF.InOn := BITGET(_IO_IX50_0_0.ValueDINT, 9);(*ШВВ. 3QF Включен*) (*REG=98.9/[COM1023:1:98]*)
GP0022_SHPT2_3QF.InEOff := BITGET(_IO_IX50_0_0.ValueDINT, 10);(*ШВВ. 3QF Аварийное отключение*) (*REG=98.10/[COM1023:1:98]*)

GP0022_SHPT2_3QS.InOff := BITGET(_IO_IX50_0_0.ValueDINT, 11);(*ШВВ. 3QS Отключен*) (*REG=98.11/[COM1023:1:98]*)
GP0022_SHPT2_3QS.InOn := NOT BITGET(_IO_IX50_0_0.ValueDINT, 11);(*ШВВ. 3QS Включен*) (*REG=98.11/[COM1023:1:98]*)

GP0022_SHPT2_5QS.InOff := BITGET(_IO_IX50_0_0.ValueDINT, 12);(*ШВВ. 5QS Отключен*) (*REG=98.12/[COM1023:1:98]*)
GP0022_SHPT2_5QS.InOn := NOT BITGET(_IO_IX50_0_0.ValueDINT, 12);(*ШВВ. 5QS Включен*) (*REG=98.12/[COM1023:1:98]*)

GP0022_SHPT2_7QF.InOff := BITGET(_IO_IX50_0_1.ValueDINT, 1);(*ШВВ. 7QF Отключен*) (*REG=99.1/[COM1023:1:98]*)
GP0022_SHPT2_7QF.InOn := NOT BITGET(_IO_IX50_0_1.ValueDINT, 1);(*ШВВ. 7QF Включен*) (*REG=99.1/[COM1023:1:98]*)

GP0022_SHPT2_8QF.InOff := BITGET(_IO_IX50_0_1.ValueDINT, 2);(*ШВВ. 8QF Отключен*) (*REG=99.2/[COM1023:1:98]*)
GP0022_SHPT2_8QF.InOn := BITGET(_IO_IX50_0_1.ValueDINT, 3);(*ШВВ. 8QF Включен*) (*REG=99.3/[COM1023:1:98]*)
GP0022_SHPT2_8QF.InEOff := BITGET(_IO_IX50_0_1.ValueDINT, 4);(*ШВВ. 8QF Аварийное отключение*) (*REG=99.4/[COM1023:1:98]*)

GP0022_SHPT2_2QF.InOff := BITGET(_IO_IX50_0_1.ValueDINT, 5);(*ШВВ. 2QF Отключен*) (*REG=99.5/[COM1023:1:98]*)
GP0022_SHPT2_2QF.InOn := BITGET(_IO_IX50_0_1.ValueDINT, 6);(*ШВВ. 2QF Включен*) (*REG=99.6/[COM1023:1:98]*)
GP0022_SHPT2_2QF.InEOff := BITGET(_IO_IX50_0_1.ValueDINT, 7);(*ШВВ. 2QF Аварийное отключение*) (*REG=99.7/[COM1023:1:98]*)

GP0022_SHPT2_4QF.InOff := BITGET(_IO_IX50_0_1.ValueDINT, 8);(*ШВВ. 4QF Отключен*) (*REG=99.8/[COM1023:1:98]*)
GP0022_SHPT2_4QF.InOn := BITGET(_IO_IX50_0_1.ValueDINT, 9);(*ШВВ. 4QF Включен*) (*REG=99.9/[COM1023:1:98]*)
GP0022_SHPT2_4QF.InEOff := BITGET(_IO_IX50_0_1.ValueDINT, 10);(*ШВВ. 4QF Аварийное отключение*) (*REG=99.10/[COM1023:1:98]*)

GP0022_SHPT2_4QS.InOff := BITGET(_IO_IX50_0_1.ValueDINT, 11);(*ШВВ. 4QS Отключен*) (*REG=99.11/[COM1023:1:98]*)
GP0022_SHPT2_4QS.InOn := NOT BITGET(_IO_IX50_0_1.ValueDINT, 11);(*ШВВ. 4QS Включен*) (*REG=99.11/[COM1023:1:98]*)

GP0022_SHPT2_6QS.InOff := BITGET(_IO_IX50_0_1.ValueDINT, 12);(*ШВВ. 6QS Отключен*) (*REG=99.12/[COM1023:1:98]*)
GP0022_SHPT2_6QS.InOn := NOT BITGET(_IO_IX50_0_1.ValueDINT, 12);(*ШВВ. 6QS Включен*) (*REG=99.12/[COM1023:1:98]*)

GP0022_SHPT2_QF9.InOff := BITGET(_IO_IX35_0_0.ValueDINT, 0);(*ШОЛ2. QF9 Отключен*) (*REG=164.0/[COM1023:1:164]*)
GP0022_SHPT2_QF9.InOn := BITGET(_IO_IX35_0_0.ValueDINT, 1);(*ШОЛ2. QF9 Включен*) (*REG=164.1/[COM1023:1:164]*)
GP0022_SHPT2_QF9.InEOff := BITGET(_IO_IX35_0_1.ValueDINT, 0);(*ШОЛ2. QF9-QF16 Аварийное отключение*) (*REG=165.0/[COM1023:1:164]*)

GP0022_SHPT2_QF10.InOff := BITGET(_IO_IX35_0_0.ValueDINT, 2);(*ШОЛ2. QF10 Отключен*) (*REG=164.2/[COM1023:1:164]*)
GP0022_SHPT2_QF10.InOn := BITGET(_IO_IX35_0_0.ValueDINT, 3);(*ШОЛ2. QF10 Включен*) (*REG=164.3/[COM1023:1:164]*)
GP0022_SHPT2_QF10.InEOff := BITGET(_IO_IX35_0_1.ValueDINT, 0);(*ШОЛ2. QF9-QF16 Аварийное отключение*) (*REG=165.0/[COM1023:1:164]*)

GP0022_SHPT2_QF11.InOff := BITGET(_IO_IX35_0_0.ValueDINT, 4);(*ШОЛ2. QF11 Отключен*) (*REG=164.4/[COM1023:1:164]*)
GP0022_SHPT2_QF11.InOn := BITGET(_IO_IX35_0_0.ValueDINT, 5);(*ШОЛ2. QF11 Включен*) (*REG=164.5/[COM1023:1:164]*)
GP0022_SHPT2_QF11.InEOff := BITGET(_IO_IX35_0_1.ValueDINT, 0);(*ШОЛ2. QF9-QF16 Аварийное отключение*) (*REG=165.0/[COM1023:1:164]*)

GP0022_SHPT2_QF12.InOff := BITGET(_IO_IX35_0_0.ValueDINT, 6);(*ШОЛ2. QF12 Отключен*) (*REG=164.6/[COM1023:1:164]*)
GP0022_SHPT2_QF12.InOn := BITGET(_IO_IX35_0_0.ValueDINT, 7);(*ШОЛ2. QF12 Включен*) (*REG=164.7/[COM1023:1:164]*)
GP0022_SHPT2_QF12.InEOff := BITGET(_IO_IX35_0_1.ValueDINT, 0);(*ШОЛ2. QF9-QF16 Аварийное отключение*) (*REG=165.0/[COM1023:1:164]*)

GP0022_SHPT2_QF13.InOff := BITGET(_IO_IX35_0_0.ValueDINT, 8);(*ШОЛ2. QF13 Отключен*) (*REG=164.8/[COM1023:1:164]*)
GP0022_SHPT2_QF13.InOn := BITGET(_IO_IX35_0_0.ValueDINT, 9);(*ШОЛ2. QF13 Включен*) (*REG=164.9/[COM1023:1:164]*)
GP0022_SHPT2_QF13.InEOff := BITGET(_IO_IX35_0_1.ValueDINT, 0);(*ШОЛ2. QF9-QF16 Аварийное отключение*) (*REG=165.0/[COM1023:1:164]*)

GP0022_SHPT2_QF14.InOff := BITGET(_IO_IX35_0_0.ValueDINT, 10);(*ШОЛ2. QF14 Отключен*) (*REG=164.10/[COM1023:1:164]*)
GP0022_SHPT2_QF14.InOn := BITGET(_IO_IX35_0_0.ValueDINT, 11);(*ШОЛ2. QF14 Включен*) (*REG=164.11/[COM1023:1:164]*)
GP0022_SHPT2_QF14.InEOff := BITGET(_IO_IX35_0_1.ValueDINT, 0);(*ШОЛ2. QF9-QF16 Аварийное отключение*) (*REG=165.0/[COM1023:1:164]*)

GP0022_SHPT2_QF15.InOff := BITGET(_IO_IX35_0_0.ValueDINT, 12);(*ШОЛ2. QF15 Отключен*) (*REG=164.12/[COM1023:1:164]*)
GP0022_SHPT2_QF15.InOn := BITGET(_IO_IX35_0_0.ValueDINT, 13);(*ШОЛ2. QF15 Включен*) (*REG=164.13/[COM1023:1:164]*)
GP0022_SHPT2_QF15.InEOff := BITGET(_IO_IX35_0_1.ValueDINT, 0);(*ШОЛ2. QF9-QF16 Аварийное отключение*) (*REG=165.0/[COM1023:1:164]*)

GP0022_SHPT2_QF16.InOff := BITGET(_IO_IX35_0_0.ValueDINT, 14);(*ШОЛ2. QF16 Отключен*) (*REG=164.14/[COM1023:1:164]*)
GP0022_SHPT2_QF16.InOn := BITGET(_IO_IX35_0_0.ValueDINT, 15);(*ШОЛ2. QF16 Включен*) (*REG=164.15/[COM1023:1:164]*)
GP0022_SHPT2_QF16.InEOff := BITGET(_IO_IX35_0_1.ValueDINT, 0);(*ШОЛ2. QF9-QF16 Аварийное отключение*) (*REG=165.0/[COM1023:1:164]*)

GP0022_SHPT2_10QF.InOff := BITGET(_IO_IX35_0_1.ValueDINT, 1);(*ШОЛ2. 10QF Отключен*) (*REG=165.1/[COM1023:1:164]*)
GP0022_SHPT2_10QF.InOn := BITGET(_IO_IX35_0_1.ValueDINT, 2);(*ШОЛ2. 10QF Включен*) (*REG=165.2/[COM1023:1:164]*)
GP0022_SHPT2_10QF.InEOff := BITGET(_IO_IX35_0_1.ValueDINT, 3);(*ШОЛ2. 10QF Аварийное отключение*) (*REG=165.3/[COM1023:1:164]*)

GP0022_SHPT2_2QS.InOff := BITGET(_IO_IX35_0_1.ValueDINT, 4);(*ШОЛ2. 2QS Отключен*) (*REG=165.4/[COM1023:1:164]*)
GP0022_SHPT2_2QS.InOn := NOT BITGET(_IO_IX35_0_1.ValueDINT, 4);(*ШОЛ2. 2QS Включен*) (*REG=165.4/[COM1023:1:164]*)

GP0022_SHPT2_QF1.InOff := BITGET(_IO_IX32_0_0.ValueDINT, 0);(*ШОЛ1. QF1 Отключен*) (*REG=78.0/[COM1023:1:78]*)
GP0022_SHPT2_QF1.InOn := BITGET(_IO_IX32_0_0.ValueDINT, 1);(*ШОЛ1. QF1 Включен*) (*REG=78.1/[COM1023:1:78]*)
GP0022_SHPT2_QF1.InEOff := BITGET(_IO_IX32_0_1.ValueDINT, 0);(*ШОЛ1. QF1-8 Аварийное срабатывание защитного аппарата*) (*REG=79.0/[COM1023:1:78]*)

GP0022_SHPT2_QF2.InOff := BITGET(_IO_IX32_0_0.ValueDINT, 2);(*ШОЛ1. QF2 Отключен*) (*REG=78.2/[COM1023:1:78]*)
GP0022_SHPT2_QF2.InOn := BITGET(_IO_IX32_0_0.ValueDINT, 3);(*ШОЛ1. QF2 Включен*) (*REG=78.3/[COM1023:1:78]*)
GP0022_SHPT2_QF2.InEOff := BITGET(_IO_IX32_0_1.ValueDINT, 0);(*ШОЛ1. QF1-8 Аварийное срабатывание защитного аппарата*) (*REG=79.0/[COM1023:1:78]*)

GP0022_SHPT2_QF3.InOff := BITGET(_IO_IX32_0_0.ValueDINT, 4);(*ШОЛ1. QF3 Отключен*) (*REG=78.4/[COM1023:1:78]*)
GP0022_SHPT2_QF3.InOn := BITGET(_IO_IX32_0_0.ValueDINT, 5);(*ШОЛ1. QF3 Включен*) (*REG=78.5/[COM1023:1:78]*)
GP0022_SHPT2_QF3.InEOff := BITGET(_IO_IX32_0_1.ValueDINT, 0);(*ШОЛ1. QF1-8 Аварийное срабатывание защитного аппарата*) (*REG=79.0/[COM1023:1:78]*)

GP0022_SHPT2_QF4.InOff := BITGET(_IO_IX32_0_0.ValueDINT, 6);(*ШОЛ1. QF4 Отключен*) (*REG=78.6/[COM1023:1:78]*)
GP0022_SHPT2_QF4.InOn := BITGET(_IO_IX32_0_0.ValueDINT, 7);(*ШОЛ1. QF4 Включен*) (*REG=78.7/[COM1023:1:78]*)
GP0022_SHPT2_QF4.InEOff := BITGET(_IO_IX32_0_1.ValueDINT, 0);(*ШОЛ1. QF1-8 Аварийное срабатывание защитного аппарата*) (*REG=79.0/[COM1023:1:78]*)

GP0022_SHPT2_QF5.InOff := BITGET(_IO_IX32_0_0.ValueDINT, 8);(*ШОЛ1. QF5 Отключен*) (*REG=78.8/[COM1023:1:78]*)
GP0022_SHPT2_QF5.InOn := BITGET(_IO_IX32_0_0.ValueDINT, 9);(*ШОЛ1. QF5 Включен*) (*REG=78.9/[COM1023:1:78]*)
GP0022_SHPT2_QF5.InEOff := BITGET(_IO_IX32_0_1.ValueDINT, 0);(*ШОЛ1. QF1-8 Аварийное срабатывание защитного аппарата*) (*REG=79.0/[COM1023:1:78]*)

GP0022_SHPT2_QF6.InOff := BITGET(_IO_IX32_0_0.ValueDINT, 10);(*ШОЛ1. QF6 Отключен*) (*REG=78.10/[COM1023:1:78]*)
GP0022_SHPT2_QF6.InOn := BITGET(_IO_IX32_0_0.ValueDINT, 11);(*ШОЛ1. QF6 Включен*) (*REG=78.11/[COM1023:1:78]*)
GP0022_SHPT2_QF6.InEOff := BITGET(_IO_IX32_0_1.ValueDINT, 0);(*ШОЛ1. QF1-8 Аварийное срабатывание защитного аппарата*) (*REG=79.0/[COM1023:1:78]*)

GP0022_SHPT2_QF7.InOff := BITGET(_IO_IX32_0_0.ValueDINT, 12);(*ШОЛ1. QF7 Отключен*) (*REG=78.12/[COM1023:1:78]*)
GP0022_SHPT2_QF7.InOn := BITGET(_IO_IX32_0_0.ValueDINT, 13);(*ШОЛ1. QF7 Включен*) (*REG=78.13/[COM1023:1:78]*)
GP0022_SHPT2_QF7.InEOff := BITGET(_IO_IX32_0_1.ValueDINT, 0);(*ШОЛ1. QF1-8 Аварийное срабатывание защитного аппарата*) (*REG=79.0/[COM1023:1:78]*)

GP0022_SHPT2_QF8.InOff := BITGET(_IO_IX32_0_0.ValueDINT, 14);(*ШОЛ1. QF8 Отключен*) (*REG=78.14/[COM1023:1:78]*)
GP0022_SHPT2_QF8.InOn := BITGET(_IO_IX32_0_0.ValueDINT, 15);(*ШОЛ1. QF8 Включен*) (*REG=78.15/[COM1023:1:78]*)
GP0022_SHPT2_QF8.InEOff := BITGET(_IO_IX32_0_1.ValueDINT, 0);(*ШОЛ1. QF1-8 Аварийное срабатывание защитного аппарата*) (*REG=79.0/[COM1023:1:78]*)

GP0022_SHPT2_9QF.InOff := BITGET(_IO_IX32_0_1.ValueDINT, 1);(*ШОЛ1. 9QF Отключен*) (*REG=79.1/[COM1023:1:78]*)
GP0022_SHPT2_9QF.InOn := BITGET(_IO_IX32_0_1.ValueDINT, 2);(*ШОЛ1. 9QF Включен*) (*REG=79.2/[COM1023:1:78]*)
GP0022_SHPT2_9QF.InEOff := BITGET(_IO_IX32_0_1.ValueDINT, 3);(*ШОЛ1. 9QF Аварийное отключение*) (*REG=79.3/[COM1023:1:78]*)

GP0022_SHPT2_1QS.InOff := BITGET(_IO_IX32_0_1.ValueDINT, 4);(*ШОЛ1. 1QS Отключен*) (*REG=79.4/[COM1023:1:78]*)
GP0022_SHPT2_1QS.InOn := NOT BITGET(_IO_IX32_0_1.ValueDINT, 4);(*ШОЛ1. 1QS Включен*) (*REG=79.4/[COM1023:1:78]*)

GP0022_SHPT2_Q1.InOff := BITGET(_IO_IX32_0_1.ValueDINT, 5);(*ШОЛ1. Q1 Отключен*) (*REG=79.5/[COM1023:1:78]*)
GP0022_SHPT2_Q1.InOn := NOT BITGET(_IO_IX32_0_1.ValueDINT, 5);(*ШОЛ1. Q1 Включен*) (*REG=79.5/[COM1023:1:78]*)
""".split('\n')


for line in code:
    marka, *args = line.split('.')
    if len(args) != 0:
        print(f"      QF3_to_TOPO({{{marka}..StOn}},{{{marka}..StOff}},{{{marka}..StDbl}},{{{marka}..StInvalid}},{{{marka}..StUnc}}), ")
    else:
        print(line)
#
# for line in code:
#     marka, *args = line.split('_LD_ALARM_SIM')
#     if len(args) != 0:
#         marka = marka.replace('_TOPO','')
#         marka= marka.replace(' ','')
#         marka = marka.replace('			','')
#         print(f"            {{{marka}..InEOff}});")
#     else:
#         print(line)