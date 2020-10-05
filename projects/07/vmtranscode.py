import sys

class VMTransCode:

	def __init__(self, filePath):
		self.file = open(filePath, 'w+')
		sys.stdout = self.file
		self.commandNum = 0
		self.fileName = None

	def close(self):
		sys.stdout = sys.__stdout__
		self.file.close()

	def setFileName(self, fileName):
		self.fileName = fileName


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

			print(f'@END{self.commandNum}')
			print('0;JMP')

			print(f'(IF_TRUE{self.commandNum})')
			print('@SP')
			print('A=M-1')
			print('A=A-1')
			print('M=0')
			print('M=!M')

			print(f'(END{self.commandNum})')
			print('0')

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


	def writeEndOfInstruction(self):
		print('(EOI_LOOP)')
		print('@EOI_LOOP')
		print('0;JMP')



				

