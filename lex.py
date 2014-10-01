# lexes scanned characters into tokens

import tok, err

class Lex(object):
	def __init__(self, scan):
		self.scan = scan
		self.list = []
		self.parenDepth = 0

	def lex(self):
		sc = self.scan
		self.list = [] # reset on every call
		while sc.next():
			pos = sc.get_pos()
			if sc.get() == '(':
				self.list.append(tok.Tok("bp", sc.emit(), pos))
				self.parenDepth += 1
				self.lex_list()
			elif sc.get() == ')':
				self.list.append(tok.Tok("ep", sc.emit(), pos))
				self.parenDepth -= 1
				if self.parenDepth > 0:
					self.lex_list()
				elif self.parenDepth < 0:
					self.parenDepth += 1 # suppresses further errors
					raise err.Err("too many end parens").err()
				else:
					return self.list
			elif sc.get() == '#':
				while sc.get() != '\n':
					sc.next()
				sc.emit() # dump coment
			else:
				dump = sc.emit() # dump
				if len(dump.strip()) > 0:
					err.Err("unknown '" + (dump if len(dump)<=10 else dump[0:10-3]+'...') + "'", pos=sc.get_pos()).err()
		return self.list

	def lex_list(self):
		sc = self.scan
		self.lex_space() # flush space
		while True:
			if not self.lex_id():
				if not self.lex_num():
					if not self.lex_str():
						break
			self.lex_space()

	def lex_id(self):
		sc = self.scan
		pos = sc.get_pos()
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
		self.list.append(tok.Tok("id", sc.emit(), pos))
		return True
	def lex_num(self):
		sc = self.scan
		pos = sc.get_pos()
		while sc.next():
			if not sc.get().isdigit():
				sc.backup()
				break
		if sc.len() == 0:
			return False
		self.list.append(tok.Tok("n", sc.emit(), pos))
		return True
	def lex_str(self):
		sc = self.scan
		pos = sc.get_pos()
		sc.next()
		if sc.get() == '"':
			while sc.next():
				if sc.get() == '"':
					break
		else:
			sc.backup()
			return False
		self.list.append(tok.Tok("str", sc.emit()[1:-1], pos))
		return True
	def lex_space(self):
		sc = self.scan
		while sc.next():
			if not sc.get().isspace():
				sc.backup()
				break
		sc.emit() # dump
	def is_symb(self, c):
		return c in [':', '!', '`', '~', '@', '#', '$', '%', '^', '&', '*', '+', '-', '=', '>', '<', '/', '{', '}', '[', ']', '.']