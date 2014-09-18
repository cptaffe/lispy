# lexes scanned characters into tokens

import scan, tok

class Lex(object):
	def __init__(self, scan):
		self.scan = scan
		self.list = []
		self.parenDepth = 0

	def lex(self):
		sc = self.scan
		self.list = [] # reset on every call
		while sc.next():
			if sc.get() == '(':
				self.list.append(tok.Tok("bp", sc.emit()))
				self.parenDepth += 1
				self.lex_list()
			elif sc.get() == ')':
				self.list.append(tok.Tok("ep", sc.emit()))
				self.parenDepth -= 1
				if self.parenDepth > 0:
					self.lex_list()
				elif self.parenDepth < 0:
					raise Exception("too many end parens")
				else:
					return self.list
			else:
				sc.emit() # dump
		return self.list

	def lex_list(self):
		sc = self.scan
		self.lex_space() # flush space
		while True:
			if not self.lex_id():
				if not self.lex_num():
					break
			self.lex_space()

	def lex_id(self):
		sc = self.scan
		if not sc.next():
			return False
		# first character must be alphabetic
		if not sc.get().isalpha() and not self.is_symb(sc.get()):
			sc.backup()
			return False
		# alphanumeric
		while sc.next():
			if not sc.get().isalnum() and not self.is_symb(sc.get()):
				sc.backup()
				break
		self.list.append(tok.Tok("id", sc.emit()))
		return True
	def lex_num(self):
		sc = self.scan
		while sc.next():
			if not sc.get().isdigit():
				sc.backup()
				break
		if sc.len() == 0:
			return False
		self.list.append(tok.Tok("n", sc.emit()))
		return True
	def lex_space(self):
		sc = self.scan
		while sc.next():
			if not self.is_space(sc.get()):
				sc.backup()
				break
		sc.emit() # dump
	def is_space(self, c):
		return c in [' ', '\t', '\n']
	def is_symb(self, c):
		return c in [':', '!', '`', '~', '@', '#', '$', '%', '^', '&', '*', '+', '-', '=', '>', '<', '/', '{', '}', '[', ']', '.']