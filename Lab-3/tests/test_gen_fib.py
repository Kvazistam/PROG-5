import sys

sys.path.append('..')
import gen_fib
import Fib_checker
def test_gen_fib1():
    gen = gen_fib.my_genn()
    assert gen.send(0) == []

def test_gen_fib2():
    gen = gen_fib.my_genn()
    assert gen.send(1) == [0]    

def test_gen_fib3():
    gen = gen_fib.my_genn()
    assert gen.send(8) == [0, 1, 1, 2, 3, 5, 8, 13]    