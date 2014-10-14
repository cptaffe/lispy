# optimizer for code

import copy, ast, tok, err

path = "/Users/cptaffe/Documents/git/lispy/"

def give_context(otree, ntree, index):
	ntree.parent = otree.parent
	otree.parent.child[index] = ntree
	return ntree

class Eval(object):
	def __init__(self, parser):
		self.parser = parser
		s = Scope()
		self.vars = Scope()
		s.add_child(self.vars, "_")
		self.vars.add_parent(s)
		self.builtins = Builtins(self)
		self.vars.add("#t", ast.Ast(tok.Tok("n", 1)))
		self.vars.add("#f", ast.Ast(tok.Tok("n", 0)))

	# Generator
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
			func = scope.in_var(tree.data.string)
			if not func:
				# builtins check
				try:
					return self.builtins.eval(tree, scope, tree.data.string)
				except KeyError:
					err.Err("undefined " + "'" + tree.data.string + "'", tree=tree).err()
			else:
				v = give_context(tree, func, 0)
				return recurse, (v, scope)

		# numbers eval to themselves
		elif typ in ["n", "str"]:
			return tree # leave alone
		else:
			err.Err("unknown type in tree", tree=tree).err()

	def eval_subs(self, tree, scope, recurse):
		tree.child = [self.eval_loop(recurse, (t, scope)) for t in tree.child]
		return tree

class Scope(object):
	def __init__(self):
		self.vars = {}
		self.parent = None
		self.child = {}
	def in_var(self, string):
		split = string.split(':')
		if len(split) > 1:
			s = self.in_scope(split[0])
			if s:
				return s.in_var(":".join(split[1:]))
			else:
				return False
		else:
			try:
				return copy.deepcopy(self.vars[string])
			except KeyError:
				if self.parent:
					return self.parent.in_var(string)
				else:
					return False
	def add(self, name, tree):
		split = name.split(':')
		if len(split) > 1:
			self.in_scope(split[0]).add(":".join(split[1:]), tree)
		else:
			self.vars[name] = tree
	def add_parent(self, scope):
		self.parent = scope
	def add_child(self, scope, string):
		self.child[string] = scope
	def in_scope(self, string):
		try:
			return self.child[string]
		except KeyError:
			if self.parent:
				return self.parent.in_scope(string)
			else:
				return False
	def __str__(self):
		import pprint
		return "\n".join(sorted([str(x) + ": " + str(pprint.pprint(self.vars[x]).pprint()) for x in self.vars]))

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
		#"!": self.eval_not_eval,
		#"`": self.eval_inactive_list,
		".": self.eval_concat,
		"{": self.eval_negate,
		"=": self.eval_equate,
		"?": self.eval_if,
		"@i": self.eval_import,
		"%": self.eval_mod,
		"scope": self.eval_scope,
		"nscope": self.eval_namedscope,
		"newscope": self.eval_newscope,
		"rescope": self.eval_rescope,
		"stack": self.eval_stack,
		"print": self.eval_print,

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
		#"noeval": self.eval_not_eval,
		#"inactive": self.eval_inactive_list,
		"concat": self.eval_concat,
		"negate": self.eval_negate,
		"equate": self.eval_equate,
		"if": self.eval_if,
		"import": self.eval_import,
		}
		self.stack = []

	# checks arguments, given vs. taken
	def check_arg(self, tree, num):
		tnum = len(tree.child)
		if tnum != num:
			err.Err("arg mismatch " + str(tnum-1) + " for " + str(num-1), tree=tree).err()

	# Call to execute builtin
	def eval(self, tree, scope, string):
		tree2 = ast.Ast(tok.Tok("ls"))
		tree2.child = tree.get_parent().child[1:]
		self.stack.append([string, copy.deepcopy(tree2)])
		return self.builtins[string], (tree.get_parent(), scope)

	def eval_stack(self, tree, scope):
		self.check_arg(tree, 1)
		import pprint
		print "\n".join([x[0] + " " + pprint.pprint(x[1]).pprint() for x in self.stack])

	# Language utilities
	def eval_scope(self, tree, scope):
		self.check_arg(tree, 1)
		print scope
		if len(scope.child):
			print ", ".join([str(x) for x in scope.child])
	def eval_namedscope(self, tree, scope):
		self.check_arg(tree, 2)
		print scope.in_scope(tree.child[1].data.string)
	def eval_rescope(self, tree, scope):
		self.check_arg(tree, 3)
		s = scope.in_scope(tree.child[1].data.string)
		if (s):
			return self.ev.eval_subs, (tree.child[2], s, self.ev.active_eval)
		else:
			err.Err("unknown scope", tree=tree).err()
	def eval_newscope(self, tree, scope):
		self.check_arg(tree, 2)
		scope.add_child(Scope(), tree.child[1].data.string)
	def eval_print(self, tree, scope):
		self.check_arg(tree, 2)
		import pprint
		print pprint.pprint(tree.child[1]).pprint()
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

	# Lambda (function) evaluation
	def eval_lambda(self, tree, scope):
		sc = Scope()
		self.check_arg(tree, 3)
		tree = tree.get_parent()
		sc.add_parent(scope) # add global scope to this scope
		lam_tree = tree.child[0]
		sc.add("self", copy.deepcopy(lam_tree)) # self keyword
		# assign keywords
		for i, v in enumerate(lam_tree.child[1].child):
			if i < len(tree.child[1:]):
				sc.add(v.data.string, self.ev.eval_loop(self.ev.active_eval, (tree.child[i+1], scope)))
			else:
				break
		# deep copy lambda, variables are not deep copied.
		return self.ev.active_eval(lam_tree.child[2], sc)

	def eval_assign(self, tree, scope):
		self.check_arg(tree, 3)
		if repr(tree.child[1].data.typ) == "id":
			name = tree.child[1].data.string
			tr = tree.child[2]
			scope.add(name, tr)
		elif repr(tree.child[1].data.typ) == "ls" and repr(tree.child[2].data.typ) == "ls":
			for i, d in enumerate(tree.child[1].child):
				name = d.data.string
				if i < len(tree.child[2].child):
					tr = tree.child[2].child[i]
				else:
					tr = copy.deepcopy(tree.child[2].child[-1])
				scope.add(name, tr)
		else:
			err.Err("cannot assign to non-var", tree=tree).err()
		return tree.child[1]
	def eval_eval(self, tree, scope):
		# double eval
		return self.ev.eval_loop(self.ev.active_eval, (self.ev.eval_loop(self.ev.active_eval, (tree.child[1], scope)), scope))

	# Mathematical operations
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
		self.check_arg(tree, 3)
		tree.child[1].data.string /= tree.child[2].data.string
		return tree.child[1]
	def eval_mod(self, tree, scope):
		for i in range(1, len(tree.child)):
				tree.child[i] = self.ev.eval_loop(self.ev.active_eval, (tree.child[i], scope))
		self.check_arg(tree, 3)
		tree.child[1].data.string %= tree.child[2].data.string
		return tree.child[1]
	def eval_negate(self, tree, scope):
		for i in range(1, len(tree.child)):
				tree.child[i] = self.ev.eval_loop(self.ev.active_eval, (tree.child[i], scope))
		self.check_arg(tree, 2)
		tree.child[1].data.string = 0 - tree.child[1].data.string
		return tree.child[1]
	#def eval_inactive_list(self, tree, scope):
	#	return self.ev.eval_loop(self.ev.eval_subs, (tree.child[1], scope, self.ev.inactive_eval))
	#def eval_not_eval(self, tree, scope):
	#	return tree.child[1]
	
	# List manipulation
	def eval_concat(self, tree, scope):
		for i in range(1, len(tree.child)):
			tree.child[i] = self.ev.eval_loop(self.ev.active_eval, (tree.child[i], scope))
		tree.child[1].child.extend(tree.child[2].child)
		return tree.child[1]
	def eval_push(self, tree, scope):
		# evaluate after push
		for i in range(1, len(tree.child)):
				tree.child[i] = self.ev.eval_loop(self.ev.active_eval, (tree.child[i], scope))
		ls = tree.child[1]
		if not repr(ls.data.typ) == "ls":
			err.Err("cannot push to non-list", tree=tree).err()
		for i in range(2, len(tree.child)):
			ls.child.append(tree.child[i])
		return ls
	def eval_pop(self, tree, scope):
		# before after push
		for i in range(1, len(tree.child)):
				tree.child[i] = self.ev.eval_loop(self.ev.active_eval, (tree.child[i], scope))
		ls = tree.child[1]
		if not repr(ls.data.typ) in ["ls", "il"]:
			err.Err("cannot pop from non-list", tree=tree).err()
		return ls.child.pop()

	# Operations involving booleans
	def eval_if(self, tree, scope):
		self.check_arg(tree, 4)
		if self.ev.eval_loop(self.ev.active_eval, (tree.child[1], scope)).data.string == 1:
			return self.ev.eval_loop(self.ev.active_eval, (tree.child[2], scope))
		else:
			return self.ev.active_eval(tree.child[3], scope)
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