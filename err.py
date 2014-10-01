

class Err(object):
	def __init__(self, st, tree=None, pos=None):
		self.msg = st
		self.tree = tree
		self.pos = pos
	def err(self):
		if self.tree is None and self.pos is None:
			raise Exception(self.msg)
		elif not self.tree is None:
			raise Exception(str(self.tree.data.pos[0]) + ":" + str(self.tree.data.pos[1]) + ": " + self.msg)
		elif not self.pos is None:
			raise Exception(str(self.pos[0]) + ":" + str(self.pos[1]) + ": " + self.msg)