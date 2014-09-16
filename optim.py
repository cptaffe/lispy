# optimizer for code

import copy

def give_context(otree, ntree, index):
	ntree.parent = otree.parent
	otree.parent.child[index] = ntree
	return ntree

class Eval(object):
	def __init__(self, tree):
		self.tree = tree
		self.vars = Scope()
		self.builtins = Builtins(self)

	def eval(self):
		return self.active_eval(self.tree, self.vars)

	def active_eval(self, tree, scope):
		if tree.data == None:
			return self.eval_subs(tree, scope, self.active_eval)
		typ = repr(tree.data.typ)
		if typ == "ls":
			# check for active list, inactive list
			if repr(tree.child[0].data.typ) == "id":
				# might be active
				return self.__eval(tree.child[0], scope, self.active_eval)
		return self.__eval(tree, scope, self.active_eval)

	def inactive_eval(self, tree, scope):
		if tree.data == None:
			return self.eval_subs(tree, scope, recurse)
		return self.__eval(tree, scope, self.inactive_eval)


	def __eval(self, tree, scope, recurse):
		typ = repr(tree.data.typ) # both astnode & tok

		# list evaluation
		if typ == "ls":
			return self.eval_subs(tree, scope, recurse)

		# evaluates identifiers
		if typ == "id":
			if not scope.is_in_var(tree.data.string):
				if not self.builtins.check(tree):
					raise Exception("undefined " + "'" + tree.data.string + "'")
				else:
					return self.builtins.eval(tree, scope)
			else:
				return recurse(give_context(tree, scope.in_var(tree.data.string).tree, 0), scope)

		# numbers eval to themselves
		elif typ == "n":
			return tree # leave alone
		else:
			raise Exception("unknown type in tree")

	def eval_subs(self, tree, scope, recurse):
		for i in range(0, len(tree.child)):
			tree.child[i] = recurse(tree.child[i], scope) # evaluate child trees
		return tree
	def is_active_var(self, tree, scope):
		return scope.is_in_var(tree.data.string) and scope.in_var(tree.data.string).tree.data.string in ["@", "lambda"]

class Scope(object):
	def __init__(self):
		self.vars = []
		self.parent = None
	def is_in_var(self, string):
		for v in self.vars:
			if v.name == string:
				return True
		if self.parent:
			return self.parent.is_in_var(string)
		return False
	def is_in_var_local(self, string):
		for v in self.vars:
			if v.name == string:
				return True
		return False
	def in_var(self, string):
		for v in self.vars:
			if v.name == string:
				return copy.deepcopy(v)
		if self.parent:
			return self.parent.in_var(string)
		return False
	def add(self, var):
		if self.is_in_var_local(var.name):
			for v in self.vars:
				if v.name == var.name:
					v.tree = var.tree
		else:
			self.vars.append(var)
	def add_child(self, scope):
		scope.parent = self
	def __str__(self):
		string = ""
		for v in self.vars:
			string += "(" + str(v.name) + ": " + str(v.tree) + ")"
		return string

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
		"add": self.eval_add,
		"sub": self.eval_sub,
		"mul": self.eval_mul,
		"div": self.eval_div,
		"+": self.eval_add,
		"-": self.eval_sub,
		"*": self.eval_mul,
		"/": self.eval_div,
		"lambda": self.eval_lambda,
		"@": self.eval_lambda,
		"!": self.eval_not_eval,
		"`": self.eval_inactive_list,
		".": self.eval_concat,
		"{": self.eval_negate,
		}
	def check(self, tree):
		if not tree.data.string in self.builtins:
			return False
		else:
			return True
	def eval(self, tree, scope):
		return self.builtins[tree.data.string](tree.get_parent(), scope)
	def eval_push(self, tree, scope):
		# evaluate after push
		for i in range(1, len(tree.child)):
				tree.child[i] = self.ev._Eval__eval(tree.child[i], scope)
		ls = tree.child[1]
		if not repr(ls.data.typ) == "ls":
			raise Exception("cannot push to non-list")
		for i in range(2, len(tree.child)):
			ls.child.append(tree.child[i])
		return ls
	def eval_pop(self, tree, scope):
		# before after push
		for i in range(1, len(tree.child)):
				tree.child[i] = self.ev._Eval__eval(tree.child[i], scope)
		ls = tree.child[1]
		if not repr(ls.data.typ) in ["ls", "il"]:
			raise Exception("cannot pop from non-list")
		return ls.child.pop()
	def eval_assign(self, tree, scope):
		if len(tree.child) != 3:
			raise Exception("incorrect number of args for assign")
		if repr(tree.child[1].data.typ) == "id":
			name = tree.child[1].data.string
			tr = tree.child[2]
			scope.add(Var(name, tr))
		elif repr(tree.child[1].data.typ) == "ls" and repr(tree.child[2].data.typ) == "ls":
			for i, d in enumerate(tree.child[1].child):
				name = d.data.string
				if i < len(tree.child[2].child):
					tr = tree.child[2].child[i]
				else:
					tr = copy.deepcopy(tree.child[2].child[-1])
				scope.add(Var(name, tr))
		else:
			raise Exception("cannot assign to non-var")
		return tree.child[1]
	def eval_eval(self, tree, scope):
		# double eval
		return self.ev.active_eval(self.ev.active_eval(tree.child[1], scope), scope)
	def eval_add(self, tree, scope):
		for i in range(1, len(tree.child)):
				tree.child[i] = self.ev.active_eval(tree.child[i], scope)
		if len(tree.child) != 3:
			raise Exception("incorrect number of args for add")
		tree.child[1].data.string += tree.child[2].data.string
		return tree.child[1]
	def eval_sub(self, tree, scope):
		for i in range(1, len(tree.child)):
				tree.child[i] = self.ev._Eval__eval(tree.child[i], scope)
		if len(tree.child) != 3:
			raise Exception("incorrect number of args for sub")
		tree.child[1].data.string -= tree.child[2].data.string
		return tree.child[1]
	def eval_mul(self, tree, scope):
		for i in range(1, len(tree.child)):
				tree.child[i] = self.ev._Eval__eval(tree.child[i], scope)
		if len(tree.child) != 3:
			raise Exception("incorrect number of args for mul")
		tree.child[1].data.string *= tree.child[2].data.string
		return tree.child[1]
	def eval_div(self, tree, scope):
		for i in range(1, len(tree.child)):
				tree.child[i] = self.ev._Eval__eval(tree.child[i], scope)
		if len(tree.child) != 3:
			raise Exception("incorrect number of args for div")
		tree.child[1].data.string /= tree.child[2].data.string
		return tree.child[1]
	def eval_lambda(self, tree, scope):
		sc = Scope()
		tree = tree.get_parent()
		if len(tree.child) != 3:
			raise Exception("incorrect number of args for lambda")
		scope.add_child(sc) # add global scope to this scope
		lam_tree = tree.child[0]
		sc.add(Var("self", lam_tree)) # self keyword
		# assign keywords
		for i, v in enumerate(lam_tree.child[1].child):
			if i < len(tree.child[1:]):
				sc.add(Var(v.data.string, tree.child[i+1]))
			else:
				break
		# deep copy lambda, variables are not deep copied.
		return self.ev.active_eval(lam_tree.child[2], sc)
	def eval_inactive_list(self, tree, scope):
		return self.ev.eval_subs(tree.child[1], scope, self.ev.inactive_eval)
	def eval_not_eval(self, tree, scope):
		return tree.child[1]
	def eval_concat(self, tree, scope):
		for i in range(1, len(tree.child)):
			tree.child[i] = self.ev.active_eval(tree.child[i], scope)
		tree.child[1].child.extend(tree.child[2].child)
		return tree.child[1]
	def eval_negate(self, tree, scope):
		for i in range(1, len(tree.child)):
				tree.child[i] = self.ev._Eval__eval(tree.child[i], scope)
		if len(tree.child) != 2:
			raise Exception("incorrect number of args for div")
		tree.child[1].data.string = 0 - tree.child[1].data.string
		return tree.child[1]



# variables
class Var(object):
	def __init__(self, name, tree):
		self.name = name
		self.tree = tree