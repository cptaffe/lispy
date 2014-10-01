# scans input from a file

import codecs

class Scan(object):
	def __init__(self, input_file):
		self.file = input_file
		self.line = ""
		self.pos = 0 # pos in characters
		# position for source purposes
		self.line_pos = 0
		self.char_pos = 0

	# implement EOF.
	def next(self):
		if len(self.line) - self.pos == 0:
			self.__next_line()
			# no info gotten
			if len(self.line) - self.pos == 0:
				return False
		self.pos += 1
		self.char_pos += 1
		return True
	def backup(self):
		if (self.pos > 0):
			self.pos -= 1
			self.char_pos -= 1
		else:
			raise Exception("cannot backup")
	def __next_line(self):
		self.line += self.file.readline()
		self.line_pos += 1
		self.char_pos = 0
	def get(self):
		return self.line[self.pos - 1]
	def emit(self):
		s = self.line[:self.pos]
		self.line = self.line[self.pos:]
		self.pos = 0
		return s
	def len(self):
		return self.pos
	def get_pos(self):
		return (self.line_pos, self.char_pos)
