# conglomeration of all stages

import lex, parse, optim, scan, pprint, codecs, sys

class lispy(object):
	def __init__(self, fn=None):
		self.fn = fn
		self.tree = None
	def eval(self):
		if self.fn == None:
			f = sys.stdin
		else:
			f = codecs.open(self.fn, encoding='utf-8')
		l = lex.Lex(scan.Scan(f)).lex()
		p = parse.Parse(l).parse()
		print pprint.pprint(p).pprint()
		self.tree = optim.Eval(p).eval()
		return self
	def __repr__(self):
		return pprint.pprint(self.tree).pprint()
	def __str__(self):
		return self.__repr__()