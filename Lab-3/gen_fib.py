import functools

def fib_elem_gen():
    """Генератор, возвращающий элементы ряда Фибоначчи"""
    a = 0
    b = 1

    while True:
        yield a
        res = a + b
        a = b
        b = res

# g = fib_elem_gen()

# while True:
#     el = next(g)
#     print(el)
#     if el > 10:
#         break
        
def fib_coroutine(g):
    @functools.wraps(g)
    def inner(*args, **kwargs):
        gen = g(*args, **kwargs)
        gen.send(None)
        return gen
    return inner
       
@fib_coroutine
def my_genn():
    """Сопрограмма"""

    while True:
        number_of_fib_elem = yield
        if number_of_fib_elem ==0:
            l=[]
        else:
            g = fib_elem_gen()
            l=[next(g) for i in range(number_of_fib_elem)]
        yield l



if __name__=='__main__':
    gen = my_genn()
    print(gen.send(4))
    
