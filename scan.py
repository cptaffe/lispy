# scans input from a file

import codecs

class Scan(object):
	def __init__(self, input_file):
		self.file = input_file
		self.line = self.file.readline();
		self.pos = 0 # pos in characters

	# implement EOF.
	def next(self):
		if len(self.line) - self.pos == 0:
			self.__next_line()
			if len(self.line) - self.pos == 0:
				return False
		self.pos += 1
		return True
	def backup(self):
		if (self.pos > 0):
			self.pos -= 1
		else:
			raise Exception("cannot backup")
	def __next_line(self):
		self.line += self.file.readline()
	def get(self):
		return self.line[self.pos - 1]
	def emit(self):
		s = self.line[:self.pos]
		self.line = self.line[self.pos:]
		self.pos = 0
		return s
	def len(self):
		return self.pos
