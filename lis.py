# conglomeration of all stages

import lex, parse, optim, scan, pprint, codecs, sys

class lispy(object):
	def __init__(self, fn=None, color=False):
		self.fn = fn
		self.evald = ""
		self.color = color
	def eval(self):
		if self.fn == None:
			f = sys.stdin
		else:
			f = codecs.open(self.fn, encoding='utf-8')
		p = parse.Parse(lex.Lex(scan.Scan(f)))
		for t in lispy_eval(p):
			if not t == None:
				print "=> " + pprint.pprint(t, self.color).pprint()
		return self
	def version(self):
		return open("version.txt", 'r').read()

# error catching iterator
class lispy_eval(object):
	def __init__(self, p):
		self.eval = optim.Eval(p).__iter__()
	def __iter__(self):
		return self
	def next(self):
		try:
			return next(self.eval)
		except Exception as e:
			# EOF
			if len(str(e)) == 0:
				exit()
			print >> sys.stderr, str(e) # print to stderr
