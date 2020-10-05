import sys
import re
from hackasmparser import HackAsmParser as HAP
from hackasmcode import HackAsmCode as HAC
from hackasmsymtbl import HackAsmSymTbl as HAST

filePath = sys.argv[1]
varPat = re.compile(r'[A-Za-z_.$:][A-Za-z0-9_.$:]*')

# First Pass
sp = HAP(filePath) # symbol parser
st = HAST()        # symbol table
lineCnt = -1

while(sp.hasMoreCommands()):
	sp.advance()
	cmdType = sp.commandType()


	if not cmdType == 'L_COMMAND': lineCnt += 1
	else:
		sym = sp.symbol()
		st.addEntry(sym, lineCnt+1)


# Second Pass
p = HAP(filePath) # parser
binCmds = []
memCnt = 16

while(p.hasMoreCommands()):
	p.advance()
	cmdType = p.commandType()

	if cmdType == 'A_COMMAND':
		sym = p.symbol()
		if re.fullmatch(varPat, sym):
			if sym in st: sym = st.getAddress(sym)
			else: 
				st.addEntry(sym, memCnt)
				sym = memCnt
				memCnt += 1
		else: sym = int(sym)

		binSym = format(int(bin(sym)[2:]), '015d')
		binCmds.append('0' + binSym)

	elif cmdType == 'L_COMMAND':
		pass

	else:
		assert cmdType == 'C_COMMAND'

		head = '111'
		c = HAC.comp(p.comp())
		d = HAC.dest(p.dest())
		j = HAC.jump(p.jump())

		binCmds.append(head+c+d+j)

saveFilePath = filePath[:-3] + 'hack'
saveFile = open(saveFilePath, 'w+')
print('\n'.join(binCmds), file=saveFile)
saveFile.close()

