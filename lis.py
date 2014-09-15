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
		#try:
		l = lex.Lex(scan.Scan(f)).lex()
		#except Exception as e:
		#	raise e
		#try:
		p = parse.Parse(l).parse()
		self.parsed = pprint.pprint(p).pprint().split('\n')
		#except Exception as e:
		#	raise Exception(str(e) + "; on this stream: \n" + str(l))
		#try:
		self.tree = optim.Eval(p).eval()
		self.evald = pprint.pprint(self.tree).pprint().split('\n')
		#except Exception as e:
			#raise Exception(str(e)+"; on this tree: \n"+pprint.pprint(p).pprint())
		return self
	def __repr__(self):
		string = ""
		for i, s in enumerate(self.parsed):
			string += s + "\x1b[37;1m => \x1b[0m" + self.evald[i]
			if i < len(self.parsed) - 1:
				string += '\n'
		return string
	def __str__(self):
		return self.__repr__()