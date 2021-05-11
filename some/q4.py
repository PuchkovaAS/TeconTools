desc = """GP0022_SHPT2_SHPN1_REG1_I_OUT	ШПН1 Стабилизатор1. Ток на выходе	84	REAL
GP0022_SHPT2_SHPN5_REG2_I_OUT	ШПН5 Стабилизатор2. Ток на выходе	112	REAL""".split('\n')

# for d in desc:
#     marka, d = d.split('\t')
#     new, marka = marka.split('GP0022_SHPT2_SHPN1_')
#     new, d = d.split('ШПН1. ')
#     print(f"""GP0022_SHPT2_SHPN3_{marka}\tШПН3. {d}""")
# DI_DIG_2A  AI_DIG_MON
for inc, d in enumerate(desc):
    marka, des, *arf = d.split('\t')

    print(f"{inc}\t2/PLC_GP_22_1BR/1/{marka}/AI_DIG_MON\t{des.split('. ')[1]}")