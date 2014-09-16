# pretty prints trees in lisp-paren like notation

import ast

class pprint(object):
	def __init__(self, tree):
		self.tree = tree
		self.string = ""
	
	def pprint(self):
		self.__pprint(self.tree)
		return self.string
	def __pprint(self, tree):
		if tree == None:
			self.string += "nil"
		elif tree.data == None:
			self.__pprint_child(tree.child, "\n")
		else:
			typ = ast.types[tree.data.typ.typ]
			if typ == "ls":
				self.string += "("
				self.__pprint_active_child(tree.child, " ")
				self.string += ")"
			elif typ == "id":
				self.string += "\x1b[32;1m" + str(tree.data.string) + "\x1b[0m"
			elif typ == "n":
				self.string += "\x1b[31;1m" + str(tree.data.string) + "\x1b[0m"
	def __pprint_child(self, ls, sep):
		return self.__pprint_inactive_child(ls, sep, 0)
	def __pprint_inactive_child(self, ls, sep, x):
		for i, c in enumerate(ls[x:]):
				self.__pprint(c)
				if i < len(ls) - (1 + x):
					self.string += sep
	def __pprint_active_child(self, ls, sep):
		if len(ls) == 0:
			self.string += "none"
			return
		x = 0
		if ls[0] != None and ast.types[ls[0].data.typ.typ] == "id":
			x = 1
			self.string += "\x1b[36;1m" + ls[0].data.string + "\x1b[0m"
			if len(ls) > 1:
				self.string += sep
		return self.__pprint_inactive_child(ls, sep, x)
