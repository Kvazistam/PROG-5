import sys

sys.path.append('..')
import Fib_checker
def test_gen_fib1():
    l = list(Fib_checker.Fib_checker([0,1,2,3,4,5,7,13,7,5, 8, 1, 0]))
    assert l == [0, 1, 2, 3, 5, 13, 5, 8, 1, 0]

def test_gen_fib2():
    l = list(Fib_checker.Fib_checker([]))
    assert l == []

def test_gen_fib4():
    l = list(Fib_checker.Fib_checker([0]))
    assert l == [0]

def test_gen_fib1():
    l = list(Fib_checker.Fib_checker([0,1,1,2,3,5,8,13,13,13,2,2,2]))
    assert l == [0,1,1,2,3,5,8,13,13,13,2,2,2]

