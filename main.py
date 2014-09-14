#! /usr/bin/env pypy

import lis, sys

# scanner, ex: "input.lsp"
#try:
if len(sys.argv) == 2:
	lispy = lis.lispy(sys.argv[0]).eval()
else:
	lispy = lis.lispy().eval()
#except Exception as e:
#	print "err: " + str(e)
#	exit(1)
print lispy