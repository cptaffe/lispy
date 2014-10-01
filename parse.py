# parser, puts list of tokens into tree form

import tok, ast, copy

class Parse(object):
	def __init__(self, lexer):
		self.lexer = lexer
		self.paren_depth = 0

	def __list_pop(self):
		if len(self.list) > 0:
			return self.list.pop()
		else:
			return None

	def parse(self):
		self.root = ast.Ast(None)
		self.list = self.lexer.lex()
		self.list.reverse()
		while len(self.list) > 0:
			self.parse_list(self.root)
		return self.root
	def parse_list(self, tree):
		t = self.__list_pop()
		if t == None:
			return
		typ_str = tok.types[t.typ.typ]
		if typ_str == "bp":
			self.paren_depth += 1
			return self.parse_in_list(tree.add(ast.Ast(tok.Tok("ls", pos=t.pos))))
		elif typ_str == "ep":
			self.paren_depth -= 1
			if self.paren_depth < 0:
				raise Exception("unmatched paren")
			elif self.paren_depth > 0:
				return self.parse_in_list(tree.get_parent())
			else:
				return self.parse_list(tree.get_parent())
		else:
			raise Exception("unrecognized token")
	def parse_in_list(self, tree):
		while True:
			t = self.__list_pop()
			if t == None:
				raise Exception("unexpected end of file")
			typ_str = tok.types[t.typ.typ]
			if typ_str in ["bp", "ep"]:
				self.list.append(t) # push back on list
				return self.parse_list(tree)
			elif typ_str in ["id", "n", "str"]:
				if typ_str == "n":
					t.string = int(t.string)
				tree.add(ast.Ast(t))
			else:
				raise Exception("unrecognized token")