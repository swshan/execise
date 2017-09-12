import collections
import functools

class memoized(object):
    '''
        
    '''
    def __init__(self, func):
        self.func = func
        self.cache = {}
        
    def __call__(self, *args):
        if not isinstance(args, collections.Hashable):
            return self.func(*args)
        if args in self.cache:
            return self.cache[args]
        else:
            value = self.func(*args)
            self.cache[args] = value
            return value
            
    def __repr__(self):
        return self.func.__doc__
    
    def __get__(self, obj, objtype):
        return functools.partial(self.__call__, obj)

@memoized
def fibonacci(n):
    if n in (0, 1):
        return n
    return fibonacci(n-1) + fibonacci(n-2)


print fibonacci(12)