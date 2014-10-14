
# Math scope
(newscope "math")

# the factorial function takes a number and recursively
# finds the factorial value of it.
(: math:! (@ (n) (if n 1 (* n (self (- n 1))))))

# the power function takes a number and the power to raise it to
(: math:^ (@ (n r) (if r n (* n (self n (- r 1))))))

(: math:square (@ (n) (^ n 2)))
(: math:cube (@ (n) (^ n 3)))