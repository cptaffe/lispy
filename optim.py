# optimizer for code

import copy, ast, tok

path = "/Users/cptaffe/Documents/git/lispy/"

def err(tree, st):
	import pprint
	raise Exception(str(pprint.pprint(tree).pprint()) + ": " + st)

def give_context(otree, ntree, index):
	ntree.parent = otree.parent
	otree.parent.child[index] = ntree
	return ntree

class Eval(object):
	def __init__(self, parser):
		self.parser = parser
		self.vars = Scope()
		self.builtins = Builtins(self)
		import ast
		self.vars.add(Var("#t", ast.Ast(tok.Tok("n", 1))))
		self.vars.add(Var("#f", ast.Ast(tok.Tok("n", 0))))

	def __iter__(self):
		return self

	def next(self):
		self.tree = self.parser.parse()
		if len(self.tree.child) > 0:
			t = self.eval_loop(self.active_eval, (self.tree, self.vars))
			return t
		else:
			raise StopIteration()

	def eval_loop(self, func, args):
		ret = func(*args)
		while True:
			if isinstance(ret, tuple):
				(func, args) = ret
				ret = func(*args)
			else:
				return ret

	def active_eval(self, tree, scope):
		if tree.data == None:
			return self.eval_subs, (tree, scope, self.active_eval)
		typ = repr(tree.data.typ)
		if typ == "ls" and len(tree.child) > 0:
			# check for active list, inactive list
			if repr(tree.child[0].data.typ) == "id":
				return self.active_eval, (tree.child[0], scope)
		return self.__eval, (tree, scope, self.active_eval)

	def inactive_eval(self, tree, scope):
		if tree.data == None:
			return self.eval_subs(tree, scope, recurse)
		return self.__eval(tree, scope, self.inactive_eval)


	def __eval(self, tree, scope, recurse):
		typ = repr(tree.data.typ) # both astnode & tok

		# list evaluation
		if typ == "ls":
			return self.eval_subs, (tree, scope, recurse)

		# evaluates identifiers
		if typ == "id":
			if not scope.is_in_var(tree.data.string):
				if not self.builtins.check(tree):
					raise Exception("undefined " + "'" + tree.data.string + "'")
				else:
					return self.builtins.eval, (tree, scope)
			else:
				v = give_context(tree, scope.in_var(tree.data.string).tree, 0)
				return recurse, (v, scope)

		# numbers eval to themselves
		elif typ in ["n", "str"]:
			return tree # leave alone
		else:
			raise Exception("unknown type in tree")

	def eval_subs(self, tree, scope, recurse):
		for i in range(0, len(tree.child)):
			tree.child[i] = self.eval_loop(recurse, (tree.child[i], scope)) # evaluate child trees
		return tree

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

		# symbolic builtins
		"->": self.eval_push,
		"<-": self.eval_pop,
		":": self.eval_assign,
		"~": self.eval_eval,
		"+": self.eval_add,
		"-": self.eval_sub,
		"*": self.eval_mul,
		"/": self.eval_div,
		"@": self.eval_lambda,
		"!": self.eval_not_eval,
		"`": self.eval_inactive_list,
		".": self.eval_concat,
		"{": self.eval_negate,
		"=": self.eval_equate,
		"?": self.eval_if,
		"@i": self.eval_import,

		# verbose builtins
		"push": self.eval_push,
		"pop": self.eval_pop,
		"def": self.eval_assign,
		"eval": self.eval_eval,
		"add": self.eval_add,
		"sub": self.eval_sub,
		"mul": self.eval_mul,
		"div": self.eval_div,
		"lambda": self.eval_lambda,
		"noeval": self.eval_not_eval,
		"inactive": self.eval_inactive_list,
		"concat": self.eval_concat,
		"negate": self.eval_negate,
		"equate": self.eval_equate,
		"if": self.eval_if,
		"import": self.eval_import,
		}
	def check(self, tree):
		if not tree.data.string in self.builtins:
			return False
		else:
			return True
	def check_arg(self, tree, num):
		tnum = len(tree.child)
		if tnum != num:
			err(tree, "arg mismatch " + str(tnum) + " for " + str(num))
	def eval(self, tree, scope):
		return self.builtins[tree.data.string](tree.get_parent(), scope)
	def eval_push(self, tree, scope):
		# evaluate after push
		for i in range(1, len(tree.child)):
				tree.child[i] = self.ev.eval_loop(self.ev.active_eval, (tree.child[i], scope))
		ls = tree.child[1]
		if not repr(ls.data.typ) == "ls":
			raise Exception("cannot push to non-list")
		for i in range(2, len(tree.child)):
			ls.child.append(tree.child[i])
		return ls
	def eval_pop(self, tree, scope):
		# before after push
		for i in range(1, len(tree.child)):
				tree.child[i] = self.ev.eval_loop(self.ev.active_eval, (tree.child[i], scope))
		ls = tree.child[1]
		if not repr(ls.data.typ) in ["ls", "il"]:
			raise Exception("cannot pop from non-list")
		return ls.child.pop()
	def eval_assign(self, tree, scope):
		self.check_arg(tree, 3)
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
		return self.ev.eval_loop(self.ev.active_eval, (self.ev.eval_loop(self.ev.active_eval, (tree.child[1], scope)), scope))
	def eval_add(self, tree, scope):
		for i in range(1, len(tree.child)):
				tree.child[i] = self.ev.eval_loop(self.ev.active_eval, (tree.child[i], scope))
		self.check_arg(tree, 3)
		tree.child[1].data.string += tree.child[2].data.string
		return tree.child[1]
	def eval_sub(self, tree, scope):
		for i in range(1, len(tree.child)):
				tree.child[i] = self.ev.eval_loop(self.ev.active_eval, (tree.child[i], scope))
		self.check_arg(tree, 3)
		tree.child[1].data.string -= tree.child[2].data.string
		return tree.child[1]
	def eval_mul(self, tree, scope):
		for i in range(1, len(tree.child)):
				tree.child[i] = self.ev.eval_loop(self.ev.active_eval, (tree.child[i], scope))
		self.check_arg(tree, 3)
		tree.child[1].data.string *= tree.child[2].data.string
		return tree.child[1]
	def eval_div(self, tree, scope):
		for i in range(1, len(tree.child)):
				tree.child[i] = self.ev.eval_loop(self.ev.active_eval, (tree.child[i], scope))
		self.check_arg(3)
		tree.child[1].data.string /= tree.child[2].data.string
		return tree.child[1]
	def eval_lambda(self, tree, scope):
		sc = Scope()
		self.check_arg(tree, 3)
		tree = tree.get_parent()
		scope.add_child(sc) # add global scope to this scope
		lam_tree = tree.child[0]
		sc.add(Var("self", copy.deepcopy(lam_tree))) # self keyword
		# assign keywords
		for i, v in enumerate(lam_tree.child[1].child):
			if i < len(tree.child[1:]):
				sc.add(Var(v.data.string, self.ev.eval_loop(self.ev.active_eval, (tree.child[i+1], scope))))
			else:
				break
		# deep copy lambda, variables are not deep copied.
		return self.ev.active_eval(lam_tree.child[2], sc)
	def eval_inactive_list(self, tree, scope):
		return self.ev.eval_loop(self.ev.eval_subs, (tree.child[1], scope, self.ev.inactive_eval))
	def eval_not_eval(self, tree, scope):
		return tree.child[1]
	def eval_concat(self, tree, scope):
		for i in range(1, len(tree.child)):
			tree.child[i] = self.ev.eval_loop(self.ev.active_eval, (tree.child[i], scope))
		tree.child[1].child.extend(tree.child[2].child)
		return tree.child[1]
	def eval_negate(self, tree, scope):
		for i in range(1, len(tree.child)):
				tree.child[i] = self.ev.eval_loop(self.ev.active_eval, (tree.child[i], scope))
		self.check_arg(tree, 2)
		tree.child[1].data.string = 0 - tree.child[1].data.string
		return tree.child[1]
	def eval_equate(self, tree, scope):
		for i in range(1, len(tree.child)):
				tree.child[i] = self.ev.eval_loop(self.ev.active_eval, (tree.child[i], scope))
		self.check_arg(tree, 3)
		b = tree.child[1].data.string == tree.child[2].data.string
		import ast
		if b:
			tree.child[1] = ast.Ast(ast.AstNode("id", "#t"))
		else:
			tree.child[1] = ast.Ast(ast.AstNode("id", "#f"))
		return tree.child[1]
	def eval_if(self, tree, scope):
		self.check_arg(tree, 4)
		if self.ev.eval_loop(self.ev.active_eval, (tree.child[1], scope)).data.string == 1:
			return self.ev.eval_loop(self.ev.active_eval, (tree.child[2], scope))
		else:
			return self.ev.active_eval(tree.child[3], scope)
	def eval_import(self, tree, scope):
		self.check_arg(tree, 2)
		import codecs, lex, parse, scan
		# get file
		f = codecs.open(path + tree.child[1].data.string.replace(':', '/') + '.lsp', encoding='utf-8')
		oldp = self.ev.parser
		newp = parse.Parse(lex.Lex(scan.Scan(f)))
		self.ev.parser = newp
		tree.child = []
		for t in self.ev:
			tree.child.append(t.child[0])
		self.ev.parser = oldp
		return tree
	def eval_rec_depth(self, tree, scope):
		print "fuck you"

# variables
class Var(object):
	def __init__(self, name, tree):
		self.name = name
		self.tree = tree