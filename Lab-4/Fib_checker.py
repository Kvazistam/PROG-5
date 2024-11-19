
class Fib_checker:
    # from gen_fib import fib_elem_gen
    def __init__(self, get_list: list) -> None:
        self.idx = 0
        self.list = get_list

    def __iter__(self):
        return self
    def __next__(self):
        while True:
            try:
                 res = self.list[self.idx]
            except IndexError:
                 raise StopIteration
            self.idx+=1
            if self.is_fibb(res):
                return res
            
    def is_fibb(self, num):
        from gen_fib import fib_elem_gen
        fib_gen = fib_elem_gen()
        fib_elem = next(fib_gen)
        while num >= fib_elem:
            if num == fib_elem:
                return True
            fib_elem = next(fib_gen)
        return False
    
print(list(Fib_checker([0,1,2,3,4,5,7,13,7,5, 8, 1, 0])))
