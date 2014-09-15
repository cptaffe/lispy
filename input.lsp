(def e eval)
(def b (def a `(1 q)))
(def q (* 2 3))
(b)
`(a)
`(q)
(def (a f) (pop b))
`(a)
`(f)

(def a (e (f)))

(def f (@ (a b) (* a b)))
(f 2 2)