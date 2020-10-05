import sys

class VMTransCode:

	def __init__(self, filePath):
		self.file = open(filePath, 'w+')
		sys.stdout = self.file
		self.commandNum = 0
		self.fileName = None
		self.functionName = 'null'

	def close(self):
		sys.stdout = sys.__stdout__
		self.file.close()

	def setFileName(self, fileName):
		self.fileName = fileName


	def writeInit(self):
		print('@256')
		print('D=A')

		print('@SP')
		print('M=D')

		self.writeCall('Sys.init', 0)

	def writeArithmetic(self, command):
		self.commandNum += 1

		print('@SP')
		print('A=M-1')

		if command == 'neg':
			print('M=-M')
			return
		elif command == 'not':
			print('M=!M')
			return

		print('D=M')
		print('A=A-1')

		if command == 'add': print('M=D+M')
		elif command == 'sub': print('M=M-D')
		elif command == 'and': print('M=D&M')
		elif command == 'or': print('M=D|M')
		else:
			print('D=M-D')
			print(f'@IF_TRUE{self.commandNum}')
			print('D;', end='')

			if command == 'eq': print('JEQ')
			elif command == 'gt': print('JGT')
			else:
				assert command == 'lt'
				print('JLT')

			print('@SP')
			print('A=M-1')
			print('A=A-1')
			print('M=0')

			print(f'@IF_END{self.commandNum}')
			print('0;JMP')

			print(f'(IF_TRUE{self.commandNum})')
			print('@SP')
			print('A=M-1')
			print('A=A-1')
			print('M=0')
			print('M=!M')

			print(f'(IF_END{self.commandNum})')

		print('@SP')
		print('M=M-1')


	def writePushPop(self, command, segment, index):
		self.commandNum += 1

		if command == 'push':
			if segment == 'constant':
				print(f'@{index}')
				print('D=A')

			else:
				if segment == 'static':
					print(f'@{self.fileName}.{index}')

				else:
					print(f'@{index}')
					print('D=A')
					print('@', end='')

					if segment == 'pointer' or segment == 'temp':
						if segment == 'pointer': print('3')
						elif segment == 'temp': print('5')
						print('A=D+A')
					else:
						if segment == 'argument': print('ARG')
						elif segment == 'local': print('LCL')
						elif segment == 'this': print('THIS')
						elif segment == 'that': print('THAT')
						print('A=D+M')

				print('D=M')

			print('@SP')
			print('A=M')
			print('M=D')

			print('@SP')
			print('M=M+1')

		else:
			if segment == 'static':
				print('@SP')
				print('A=M-1')
				print('D=M')
				print(f'@{self.fileName}.{index}')
				print('M=D')

			else:
				print(f'@{index}')
				print('D=A')
				print('@', end='')

				if segment == 'pointer' or segment == 'temp':
					if segment == 'pointer': print('3')
					elif segment == 'temp': print('5')
					print('D=D+A')
				else:
					if segment == 'argument': print('ARG')
					elif segment == 'local': print('LCL')
					elif segment == 'this': print('THIS')
					elif segment == 'that': print('THAT')
					print('D=D+M')

				print('@R13')
				print('M=D')

				print('@SP')
				print('A=M-1')
				print('D=M')

				print('@R13')
				print('A=M')
				print('M=D')

			print('@SP')
			print('M=M-1')


	def writeLabel(self, label):
		self.commandNum += 1
		print(f'({self.functionName}${label})')


	def writeGoto(self, label):
		self.commandNum += 1
		print(f'@{self.functionName}${label}')
		print('0;JMP')


	def writeIf(self, label):
		self.commandNum += 1
		print('@SP')
		print('A=M-1')
		print('D=M')

		print('@SP')
		print('M=M-1')

		print(f'@{self.functionName}${label}')
		print('D;JNE') 

	def _writePushSymbol(self, sym, **kwargs):
		print(f'@{sym}')

		if 'isConst' in kwargs:
			if kwargs['isConst']: print('D=A')
		else: print('D=M')

		print('@SP')
		print('A=M')
		print('M=D')

		print('@SP')
		print('M=M+1')


	def writeCall(self, toCallfnName, numArgs):
		self.commandNum += 1

		return_address = f'RETURN_A{self.commandNum}'
		self._writePushSymbol(return_address, isConst=True)

		self._writePushSymbol('LCL')
		self._writePushSymbol('ARG')
		self._writePushSymbol('THIS')
		self._writePushSymbol('THAT')

		# ARG = SP-n-5
		print(f'@{numArgs+5}')
		print('D=A')

		print('@SP')
		print('D=M-D')

		print('@ARG')
		print('M=D')

		# LCL = SP
		print('@SP')
		print('D=M')

		print('@LCL')
		print('M=D')

		print(f'@{toCallfnName}')
		print('0;JMP')
		print(f'({return_address})')


	def writeFunction(self, functionName, numLocals):
		self.commandNum += 1

		self.functionName = functionName
		print(f'({functionName})')

		for i in range(numLocals):
			self._writePushSymbol('0', isConst=True)


	def writeReturn(self):
		self.commandNum += 1

		# FRAME = LCL ; R14 corresponds to FRAME
		print('@LCL')
		print('D=M')

		print('@R14')
		print('M=D')

		# RET = *(FRAME - 5) ; R15 corresponds to RET
		print('@5')
		print('A=D-A')
		print('D=M')

		print('@R15')
		print('M=D')

		# *ARG = pop() and SP = ARG+1
		print('@SP')
		print('A=M-1')
		print('D=M')

		print('@ARG')
		print('A=M')
		print('M=D')
		print('D=A')

		print('@SP')
		print('M=D+1')

		# Restore THAT, THIS, ARG, LOCAL
		for sym in 'THAT THIS ARG LCL'.split():
			print('@R14')
			print('AM=M-1')
			print('D=M')

			print(f'@{sym}')
			print('M=D')

		# Goto return address
		print('@R15')
		print('A=M')
		print('0;JMP')


				

