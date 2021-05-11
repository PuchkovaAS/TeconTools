data = """GP0022_SHPT1_SHOL1_U_SEC1	ШОЛ1. Напряжение на шине SEC1
GP0022_SHPT1_SHOL1_U_AB	ШОЛ1. Напряжение АБ
GP0022_SHPT1_SHOL1_U_PG	ШОЛ1. Напряжение между + и землей
GP0022_SHPT1_SHOL1_U_MG	ШОЛ1. Напряжение между - и землей
GP0022_SHPT1_SHOL1_dU	ШОЛ1. Перекос по полюсам
GP0022_SHPT1_SHOL1_I_OUT	ШОЛ1. Значение тока генерируемое в сеть
GP0022_SHPT1_SHOL1_C_SOPT	ШОЛ1. Емкость СОПТ
GP0022_SHPT1_SHOL1_R_P	ШОЛ1. Сопротивление изоляции по плюсовой шине
GP0022_SHPT1_SHOL1_R_M	ШОЛ1. Сопротивление изоляции по минусовой шине
GP0022_SHPT1_SHOL1_R	ШОЛ1. Общее сопротивление изоляции""".split('\n')


for num, dat in enumerate(data):
    marka, desc = dat.split('\t')
    desc = desc.split('ШОЛ1. ')[1]
    print(f"{num + 1}	2/PLC_GP_22_1BR/1/{marka}/AI_DIG_MON	{desc}")