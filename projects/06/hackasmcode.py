class HackAsmCode:
	comp_d = {
		'0'   : '101010',
		'1'   : '111111',
		'-1'  : '111010',
		'D'   : '001100',
		'A'   : '110000',
		'!D'  : '001101',
		'!A'  : '110001',
		'-D'  : '001111',
		'-A'  : '110011',
		'D+1' : '011111',
		'A+1' : '110111',
		'D-1' : '001110',
		'A-1' : '110010',
		'D+A' : '000010',
		'D-A' : '010011',
		'A-D' : '000111',
		'D&A' : '000000',
		'D|A' : '010101',
	}

	jump_d = {
		'null' : '000',
		'JGT'  : '001',
		'JEQ'  : '010',
		'JGE'  : '011',
		'JLT'  : '100',
		'JNE'  : '101',
		'JLE'  : '110',
		'JMP'  : '111',
	}

	def dest(mnemonic):
		if mnemonic == 'null': return '000'
		else:
			d1 = d2 = d3 = '0'
			if 'A' in mnemonic: d1 = '1'
			if 'M' in mnemonic: d3 = '1' 
			if 'D' in mnemonic: d2 = '1'
			return d1+d2+d3


	@classmethod
	def comp(cls, mnemonic):
		a ='0'
		mnem_cpy = mnemonic

		if 'M' in mnemonic: 
			a = '1'
			mnem_cpy = mnemonic.replace('M', 'A')

		c = cls.comp_d[mnem_cpy]
		return a+c


	@classmethod
	def jump(cls, mnemonic): return cls.jump_d[mnemonic]


