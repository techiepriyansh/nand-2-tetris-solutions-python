import os
import sys
import ntpath
import glob
from vmtransparser import VMTransParser as VMTP
from vmtranscode import VMTransCode as VMTC

def writeCode(c, vmFilePath):		
	vmFileName = ntpath.basename(vmFilePath)[:-3]

	p = VMTP(vmFilePath)
	c.setFileName(vmFileName)

	while(p.hasMoreCommands()):
		p.advance()
		cmdType = p.commandType()

		if cmdType == 'C_ARITHMETIC':
			c.writeArithmetic(p.arg1())
		elif cmdType == 'C_PUSH':
			c.writePushPop('push', p.arg1(), p.arg2())
		elif cmdType == 'C_POP':
			c.writePushPop('pop', p.arg1(), p.arg2())
		elif cmdType == 'C_LABEL':
			c.writeLabel(p.arg1())
		elif cmdType == 'C_GOTO':
			c.writeGoto(p.arg1())
		elif cmdType == 'C_IF':
			c.writeIf(p.arg1())
		elif cmdType == 'C_CALL':
			c.writeCall(p.arg1(), int(p.arg2()))
		elif cmdType == 'C_FUNCTION':
			c.writeFunction(p.arg1(), int(p.arg2()))
		else:
			assert cmdType == 'C_RETURN'
			c.writeReturn()


if __name__ == "__main__":

	inPath = sys.argv[1]

	if os.path.isdir(inPath):
		vmFiles = glob.glob(inPath + '/*.vm')

		inPathDirName = ntpath.basename(inPath)
		saveFilePath = f'{inPath}/{inPathDirName}.asm'

		c = VMTC(saveFilePath)
		c.writeInit() 
		for vmFile in vmFiles:
			writeCode(c, vmFile)

		c.close()

	else:
		saveFilePath = inPath[:-2] + 'asm'

		c = VMTC(saveFilePath)
		c.writeInit()
		writeCode(c, inPath)

		c.close()

