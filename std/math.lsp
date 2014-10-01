
# the factorial function takes a number and recursively
# finds the factorial value of it.
(: ! (@ (n) (if n 1 (* n (self (- n 1))))))

# the power function takes a number and the power to raise it to
(: ^ (@ (n r) (if r n (* n (self n (- r 1))))))

(: square (@ (n) (^ n 2)))
(: cube (@ (n) (^ n 3)))