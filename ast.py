# Abstract Syntax Tree

class Ast(object):
	def __init__(self, data):
		self.data = data
		self.child = []
		self.parent = None
	def add(self, node):
		self.child.append(node)
		node.add_par(self)
		return node
	def add_par(self, node):
		self.parent = node
	def get_child(self, index=0):
		return self.child[index]
	def get_parent(self):
		return self.parent
	def __repr__(self):
		return str(self.data) + str(self.child)

# ast node 

types = [
"ls", # list
"il", # inactive list
"ne", # not evaluated
"id", # identifier
"n", # number
]

class AstTyp(object):
	def __init__(self, typ):
		# fucked up enum type deal
		self.typ = types.index(typ)
		# define specifics of each type
	def __repr__(self):
		return types[self.typ]

class AstNode(object):
	def __init__(self, typ, string=None):
		self.typ = AstTyp(typ)
		self.string = string
	def __repr__(self):
		if self.string != None:
			string = "(" + repr(self.typ) + ":\"" + str(self.string) + "\")"
		else:
			string = "(" + repr(self.typ) + ")"
		return string