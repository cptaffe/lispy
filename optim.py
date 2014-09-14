# optimizer for code

import copy

class Eval(object):
	def __init__(self, tree):
		self.tree = tree
		self.vars = [] # var dict
		self.builtins = Builtins(self)

	def eval(self):
		return self.__eval(self.tree)

	def __eval(self, tree):
		if tree.data == None:
			return self.eval_inactive_subs(tree)
		typ = repr(tree.data.typ) # both astnode & tok
		if typ == "id":
			if not self.is_in_var(tree.data.string):
				return tree
				#raise Exception("undefined " + "'" + tree.data.string + "'")
			else:
				return self.__eval(self.in_var(tree.data.string).tree)
		elif typ == "ls":
			return self.eval_subs(tree)
		elif typ == "il":
			return tree.child[0]
		elif typ == "n":
			return tree # leave alone
		else:
			raise Exception("unknown type in tree")

	def eval_inactive_subs(self, tree):
		for i in range(0, len(tree.child)):
			tree.child[i] = self.__eval(tree.child[i]) # evaluate child trees
		return tree
	def eval_subs(self, tree):
		if repr(tree.child[0].data.typ) == "id":
			return self.active_eval(tree.child[0])
		else:
			raise Exception("list has no activator")
	def active_eval(self, tree):
		typ = repr(tree.data.typ) # both astnode & tok
		if typ == "id":
			if not self.is_in_var(tree.data.string):
				if not self.builtins.check(tree):
					return
					#raise Exception("undefined " + "'" + tree.data.string + "'")
				else:
					return self.builtins.eval(tree)
			else:
				return self.active_eval(self.give_context(tree, self.in_var(tree.data.string).tree, 0))
		else:
			return self.__eval(tree)
	def is_in_var(self, string):
		for v in self.vars:
			if v.name == string:
				return True
		return False
	def in_var(self, string):
		for v in self.vars:
			if v.name == string:
				return copy.deepcopy(v)
		return False
	def give_context(self, otree, ntree, index):
		ntree.parent = otree.parent
		otree.parent.child[index] = ntree
		return ntree

class Builtins(object):
	def __init__(self, ev):
		self.ev = ev
		# builtins used as list activators, symbolic and verbose
		self.builtins = {
		"push": self.eval_push,
		"pop": self.eval_pop,
		"->": self.eval_push,
		"<-": self.eval_pop,
		"def": self.eval_assign,
		"eval": self.eval_eval,
		":": self.eval_assign,
		"~": self.eval_eval,
		}
	def check(self, tree):
		if not tree.data.string in self.builtins:
			return False
		else:
			return True
	def eval(self, tree):
		return self.builtins[tree.data.string](tree.get_parent())
	def eval_push(self, tree):
		# evaluate after push
		for i in range(1, len(tree.child)):
				tree.child[i] = self.ev._Eval__eval(tree.child[i])
		ls = tree.child[1]
		if not repr(ls.data.typ) == "ls":
			raise Exception("cannot push to non-list")
		for i in range(2, len(tree.child)):
			ls.child.append(tree.child[i])
		return ls
	def eval_pop(self, tree):
		# before after push
		for i in range(1, len(tree.child)):
				tree.child[i] = self.ev._Eval__eval(tree.child[i])
		ls = tree.child[1]
		if not repr(ls.data.typ) in ["ls", "il"]:
			raise Exception("cannot pop from non-list")
		return ls.child.pop()
	def eval_assign(self, tree):
		if len(tree.child) != 3:
			raise Exception("incorrect number of args for assign")
		if not repr(tree.child[1].data.typ) == "id":
			raise Exception("cannot assign to non-id")
		name = tree.child[1].data.string
		tr = tree.child[2]
		self.ev.vars.append(Var(name, tr))
		return tree.child[1]
	def eval_eval(self, tree):
		# double eval
		return self.ev._Eval__eval(self.ev._Eval__eval(tree.child[1]))

# variables
class Var(object):
	def __init__(self, name, tree):
		self.name = name
		self.tree = tree