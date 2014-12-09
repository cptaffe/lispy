lispy
=====

<img src="https://raw.githubusercontent.com/cptaffe/lispy/gh-pages/images/lispy_icon_128.png" height=60px></img>

lisp-like language interpreter written in python.

As of recently, the recursive nature of the optimizer has been flattened, using function and tuple returns to the looping evaluator which keeps the stack near one for non-recursive programs.

## How to

If you want to run stuff do:
```sh
./lispy
```
Note: this uses pypy, so if you don't have pypy, you can either edit the shebang or do:
```sh
python lispy
```

For more info, check the [lispy wiki](//github.com/cptaffe/lispy/wiki)
