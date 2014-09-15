# token class 

types = [
"bt", # backtick
"ex", # exclamation (!)
"bp", # beginning paren
"ep", # ending paren
"id", # identifier
"n", # number
]

class TokTyp(object):
	def __init__(self, typ):
		# fucked up enum type deal
		self.typ = types.index(typ)
		# define specifics of each type
	def __repr__(self):
		return types[self.typ]

class Tok(object):
	def __init__(self, typ, string):
		self.typ = TokTyp(typ)
		self.string = string
	def __repr__(self):
		return "(" + repr(self.typ) + ":\"" + str(self.string) + "\")"
