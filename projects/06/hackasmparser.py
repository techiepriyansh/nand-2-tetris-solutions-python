import sys
import re

class HackAsmParser:

	def __init__(self, inFilePath):
		inFile = open(inFilePath, "r")
		self.lines = self.clean(list(inFile))
		inFile.close()

		self.lineNum = -1
		self.lastLine = len(self.lines) - 1

		self.currLine = None


	def clean(self, rawLines):
		wspPat = re.compile(r'\s+')
		commentPat = re.compile(r'//.*')

		cleanLines = []

		for line in rawLines:
			line = re.sub(wspPat, '', line)
			line = re.sub(commentPat, '', line)
			if line: cleanLines.append(line)

		return cleanLines


	def hasMoreCommands(self):
		return self.lineNum < self.lastLine


	def advance(self):
		self.lineNum += 1
		self.currLine = self.lines[self.lineNum]


	def commandType(self):
		if '@' in self.currLine: return 'A_COMMAND'
		elif '(' in self.currLine: return 'L_COMMAND'
		else: return 'C_COMMAND'


	def symbol(self):
		if '@' in self.currLine: return self.currLine[1:]
		else: return self.currLine[1:-1]


	def dest(self):
		if '=' in self.currLine: return self.currLine.split('=')[0]
		else: return 'null'


	def comp(self):
		comp_string = self.currLine

		if '=' in comp_string: comp_string = comp_string.split('=')[1]
		if ';' in comp_string: comp_string = comp_string.split(';')[0]

		return comp_string


	def jump(self):
		if ';' in self.currLine: return self.currLine.split(';')[1]
		else: return 'null'






