# syntax analyzer checks if code is legit

import tok, ast

class SyntAn(object):
	def __init__(self, tree):
		if type(tree) is ast.Ast:
			self.tree = tree
		else:
			raise Exception("tree not of type ast.Ast")

	# short for analyze
	def anal():
		print "trollolololol"