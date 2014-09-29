# conglomeration of all stages

import lex, parse, optim, scan, pprint, codecs, sys

class lispy(object):
	def __init__(self, fn=None):
		self.fn = fn
		self.evald = ""
	def eval(self):
		if self.fn == None:
			f = sys.stdin
		else:
			f = codecs.open(self.fn, encoding='utf-8')
		p = parse.Parse(lex.Lex(scan.Scan(f)))
		for t in lispy_eval(p):
			if not t == None:
				print pprint.pprint(t).pprint()
		return self

# error catching iterator
class lispy_eval(object):
	def __init__(self, p):
		self.eval = optim.Eval(p).__iter__()
	def __iter__(self):
		return self
	def next(self):
		try:
			return self.eval.next()
		except Exception as e:
			# EOF
			if len(str(e)) == 0:
				exit()
			print "err: " + str(e)