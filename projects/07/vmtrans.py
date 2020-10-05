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
		else:
			pass # complete this


if __name__ == "__main__":

	inPath = sys.argv[1]

	if os.path.isdir(inPath):
		vmFiles = glob.glob(inPath + '/*.vm')

		inPathDirName = ntpath.basename(inPath)
		saveFilePath = f'{inPath}/{inPathDirName}.asm'

		c = VMTC(saveFilePath) 
		for vmFile in vmFiles:
			writeCode(c, vmFile)

		c.writeEndOfInstruction()
		c.close()

	else:
		saveFilePath = inPath[:-2] + 'asm'

		c = VMTC(saveFilePath)
		writeCode(c, inPath)

		c.writeEndOfInstruction()
		c.close()

