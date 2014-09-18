
the factorial function takes a number and recursively
finds the factorial value of it.
(: fac (@ (n) (if n 1 (* n (self (- n 1))))))

the square function takes a number and multiplies it
by itself.
(: sqr (@ (a) (pwr a 2)))

the power function takes a number and the power to raise it to
(: pwr (@ (n r) (if r n (* n (self n (- r 1))))))