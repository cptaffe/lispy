<!-- Intro -->
title: Introduction
build_lists: true

This is an overview of an ongoing project I've been working on for around six months.

- The Basilisk Langauge
- Overview of how an interpreter works
- Specifics of lispy

---
<!-- Basilisk Language-->
title: The Basilisk Language
subtitle: An Overview
class: segue dark nobackground

---

title: S-expressions 
subtitle: much parens

S-expressions are also known as encapsulated polish notation.

This follows the pattern operator, oparands.

<pre class="prettyprint" data-lang="lisp">
	(+ 1 2)
	(add 1 2)
</pre>

I chose s-expressions because they are simple to parse into a tree.

---

title: Grammar 
subtitle: language specification

Basilisk's language spec is a bit more specific.

<pre class="prettyprint" data-lang="ebnf">
	operator = identifier | (symbol {symbol});
	argument = identifier | number | char | string;
	s-expression = "(" [whitespace] operator {whitespace argument} [whitespace] ")";
</pre>

+ identifier (or id) is a variable
+ symbols are +, -, etc.
+ numbers, chars, and strings are their respective literals.

---

title: Grammar 
subtitle: language specification

Some examples of valid & invalid grammars.

<pre class="prettyprint" data-lang="lisp">
	(+ 1 2) # valid
	(add 1 2) # valid
	(add) # valid
	(+a 1 2) # invalid
	(1 1 1) # invalid
</pre>

In lispy, a list with no operator is shorthand for a data list.

---

<!-- How an interpreter works -->
title: Interpreter
subtitle: How it works
class: segue dark nobackground

---

title: How an interpreter works 
subtitle: workflow

An interpreter usually consists of several stages:

+ Lexical Analysis (lexer)
+ Syntactic Analysis (parser)
+ Interpretation

---

title: How an interpreter works 
subtitle: Lexical Analysis

A lexer reads an input (usually a file) and produces tokens.

A typical lexer:

stream of characters -> lexer -> tokens

<pre class="prettyprint" data-lang="lisp">
	(+ 1 2)
</pre>

<pre class="prettyprint" data-lang="json">
	[
		{typ: bp, str: "("},
		{typ: id, str: "+"},
		{typ: n, str: "1"},
		{typ: n, str: "2"},
		{typ: ep, str: ")"}
	]
</pre>

---

title: How an interpreter works 
subtitle: Syntactical Analysis

A parser reads tokens and builds an abstract syntax tree (AST).

An ast usually looks like this:

![Abstract Syntax Tree](http://www.redhat.com/magazine/002dec04/features/gcc/figs/ast.png)

---

title: How an interpreter works 
subtitle: Interpretation

In the interpretation part you take the tree and evaluate it.

If all the symbols are defined, this should yield a tree in the form of a basic type.

<pre class="prettyprint" data-lang="lisp">
	(+ 1 2) # => 3
	(+ 1 b) # => 2:5: undefined 'b'
	(+ 1 (- 4 3)) # => 2
</pre>

---

<!-- Lispy -->
title: lispy
subtitle: it's pretty awesome
class: segue dark nobackground

---

title: Lazy Evaluation
subtitle: storing work for later

Keep in mind, lispy is a work in progress.

Lazy evaluation is the practice of storing the unevalutated tree in memory (the symbol table) for evaluation when needed.

<pre class="prettyprint" data-lang="lisp">
	(def a (+ 1 b)) # => a
	(a) # => 1:12: undefined 'b'
	(def b 1) # => b
	(a) # => 2
</pre>

When a is assigned, it is stored as (+1 b), which is evaluated on lines 2 and 4.

---

title: Lambdas
subtitle: scoped execution

Lambdas are the way functions are done in lispy, they get their own scope and are evaluated lazily with input.

Since all data is immutable, a lambda is reevaluated every time you call it.

<pre class="prettyprint" data-lang="lisp">
	# example of scoping
	(def func
		(lambda ()
			(def a 2))) # => func
	(def a 4) # => a
	(func) # => a
	(a) # => 4
</pre>

---

title: Lambdas
subtitle: recursion

Within the scope of a lambda, a variable called self is set with the value of itself. In this way, one can recurse.

<pre class="prettyprint" data-lang="lisp">
	(def ! 
		(lambda (n) 
			(if n 
				1 (* n (self (- n 1)))))) # => !
	(! 40) # => 815915283247897734345611269596115894272000000000
</pre>

---

title: Statement based execution
subtitle: overview

Statement based execution is a pretty neat way to interact with the interpreter. It's based on the standard REPL idea (read, evaluate, print), but intelligently.

Lispy's evaluation module calls the parser, which calls the lexer for new tokens, which returns when a full statement has been entered.

It also uses a pretty printer to print output in the syntax used for input.

<pre class="prettyprint" data-lang="lisp">
	(+ 1 2)
	3
	(+
	2 3)
	5
	(noeval (+ 1 2))
	(+ 1 2) # tree is returned, pretty printed
</pre>

---

title: REPL utility
subtitle: usage

REPL (read, eval, print loop) is a style of interpreter I use.

<object width="640" height="390">
  <param name="movie"
         value="https://www.youtube.com/v/2f6U5yGRFyk?version=3&autoplay=1&autohide=1&rel=0"></param>
  <param name="allowScriptAccess" value="always"></param>
  <embed src="https://www.youtube.com/v/2f6U5yGRFyk?version=3&autoplay=1&autohide=1&rel=0"
         type="application/x-shockwave-flash"
         allowscriptaccess="always"
         width="640" height="390"></embed>
</object>
