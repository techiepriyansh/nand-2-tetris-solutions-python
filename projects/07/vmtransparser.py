import sys
import re

class VMTransParser:

	def __init__(self, inFilePath):
		inFile = open(inFilePath, "r")
		self.lines = self.clean(list(inFile))
		inFile.close()

		self.lineNum = -1
		self.lastLine = len(self.lines) - 1

		self.currLine = None


	def clean(self, rawLines):
		commentPat = re.compile(r'//.*')

		cleanLines = []

		for line in rawLines:
			line = re.sub(commentPat, '', line)
			line.strip()
			line = ' '.join(line.split())
			if line: cleanLines.append(line)

		return cleanLines


	def hasMoreCommands(self):
		return self.lineNum < self.lastLine


	def advance(self):
		self.lineNum += 1
		self.currLine = self.lines[self.lineNum]


	def commandType(self):
		if 'push' in self.currLine: return 'C_PUSH'
		elif 'pop' in self.currLine: return 'C_POP'
		elif 'label' in self.currLine: return 'C_LABEL'
		elif 'if-goto' in self.currLine : return 'C_IF'
		elif 'goto' in self.currLine : return 'C_GOTO'
		elif 'function' in self.currLine: return 'C_FUNCTION'
		elif 'call' in self.currLine : return 'C_CALL'
		elif 'return' in self.currLine: return 'C_RETURN'
		else: return 'C_ARITHMETIC'


	def arg1(self):
		if self.commandType() == 'C_ARITHMETIC': return self.currLine
		else: return self.currLine.split()[1]

	def arg2(self): return self.currLine.split()[2]


