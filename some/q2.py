data = """GP0020_PISA2_AL	Авария кабеля датчика PISA 2
GP0020_PISA2_MIN	PISA 2 давление min
GP0020_PISA2_MAX	PISA 2 давление MAX
GP0020_PISA6_AL	Авария кабеля датчика PISA 6
GP0020_PISA6_MIN	PISA 6 давление min
GP0020_PISA6_MAX	PISA 6 давление MAX
GP0020_PISA9_MIN	PISA-9 давление min
GP0020_PISA9_MAX	PISA-9 давление MAX
GP0020_PISA10_MIN	PISA-10 давление min
GP0020_PISA10_MAX	PISA-10 давление MAX
GP0020_PISA11_MIN	PISA-11 давление min
GP0020_PISA11_MAX	PISA-11 давление MAX
GP0020_PISA3_MIN	PISA-3 давление min
GP0020_PISA3_MAX	PISA-3 давление MAX
GP0020_PISA7_MIN	PISA-7 давление min
GP0020_PISA7_MAX	PISA-7 давление MAX
GP0020_PISA1_AL	авария кабеля датчика PISA-1
GP0020_PISA1_MIN	PISA-1 давление min
GP0020_PISA1_MAX	PISA-1 давление MAX
GP0020_PISA5_AL	Авария кабеля датчика PISA-5
GP0020_PISA5_MIN	PISA-5 давление min
GP0020_PISA5_MAX	PISA-5 давление MAX
GP0020_PISA4_MIN	PISA-4 давление min
GP0020_PISA4_MAX	PISA-4 давление MAX
GP0020_PISA8_MIN	PISA-8 давление min
GP0020_PISA8_MAX	PISA-8 давление MAX
GP0020_PISA12_MIN	PISA-12 давление min
GP0020_PISA12_MAX	PISA-12 давление MAX
GP0020_PISA13_MIN	PISA-13 давление min
GP0020_PISA13_MAX	PISA-13 давление MAX
GP0020_PISA14_MIN	PISA-14 давление min
GP0020_PISA14_MAX	PISA-14 давление MAX""".split('\n')

for dat in data:
    makr, comment = dat.split('	')
    print(f"""1	2/ICore_2/1/{makr}/DI_DIG_2A	{comment}""")