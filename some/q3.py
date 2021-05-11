marks = """PLC_GP_22_G101
PLC_GP_22_G102
PLC_GP_22_G103
PLC_GP_22_G104
PLC_GP_22_SQ
PLC_GP_22_QF101
PLC_GP_22_QF102
PLC_GP_22_K101
PLC_GP_22_K102""".split('\n')


for chanel, mark in enumerate(marks):
    print(f"""{mark}( <<[1] CDI32V > канал {chanel}>>.ValueBOOL, <<[1] CDI32V > канал {chanel}>>.Status);""")