data = """65434	Время блока
65526	Ктт
65527	Ктт3I0""".split('\n')

obj = 2460
start = 15740

for num, dat in enumerate(data):
    reg1, name = dat.split('\t')
    # [- группа 3 -] Входные регистры (Input Registers)
    # print(f"""{start + num}	{name}		{start + num}	{obj}	{name}	7	0	.Reg_F4_0x0001_{str(num + 1).rjust(3,'0')}	{name}	1	0		0	R;10;100	0	0	0	0	None	None	None	None	None	None	None	None	None	None	None	None	None	None	None	None	None	None	None	None	None	None	None	None	None	None	None	None	None""")

    # [- группа 4 -] Регистры хранения (Holding Registers)
    print(f"""{start + num}	{name}		{start + num}	{obj}	{name}	7	0	.Reg_F3_0xFFF5_{reg1}	{name}\t1\t6\t\t0\tR;10;100	0	0	0	0	None	None	None	None	None	None	None	None	None	None	None	None	None	None	None	None	None	None	None	None	None	None	None	None	None	None	None	None	None""")

    # [- группа 1 -] Дискретные входы (Discrete Inputs)
    # print(f"""{start  + num}	{name}		{start  + num}	{obj}	{name}	9	0	.Bit_F2_0x0001_{reg1.rjust(3,'0')}	{name}	0	2		0	R;10;100	1	0	0	0		8372		8372	{start  + num}		Исчезновение	57		0	0		0	0	-1	8373		8373	{start  + num}		Появление	30		0	1		0	0	-1""")


    # [- группа 2 -] Битовые сигналы (Coils)
    # print(f"""{start + num}	{name}		{start + num}	{obj}	{name}	9	0	.Bit_F1_0x0001_{reg1.rjust(3,'0')}	{name}	0	12		1	R;10;100	3	0	0	0		8374		8374	{start  + num}		Деактивировать	-5		0	0		0	0	-1	8375		8375	{start  + num}		Активировать	-5		0	1		0	0	-1""")
