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
		#try:
		p = parse.Parse(lex.Lex(scan.Scan(f)))
		#except Exception as e:
		#	raise Exception(str(e) + "; on this stream: \n" + str(l))
		#try:
		for t in optim.Eval(p):
			print pprint.pprint(t).pprint()
		return self