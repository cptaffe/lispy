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