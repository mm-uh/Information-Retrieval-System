from typing import List, TypeVar
import collections
import functools

T = TypeVar('T')

def binary_search(collection: List[T], value: T) -> int:
    length: int = len(collection)
    offset: int = length // 2
    index: int = 0
    while collection[index] != value:
        if offset == 0:
            return -1 
        if index + offset < length and collection[index + offset] <= value:
            index += offset
        else:
            offset = offset // 2
    return index


def average(values: List[T]) -> float:
    length = len(values)
    return sum(values) / length
        
   
class memoized(object):
    '''Decorator. Caches a function's return value each time it is called.
    If called later with the same arguments, the cached value is returned
    (not reevaluated).
    '''
    def __init__(self, func):
        self.func = func
        self.cache = {}
    def __call__(self, *args):
        if not isinstance(args, collections.Hashable):
        # uncacheable. a list, for instance.
        # better to not cache than blow up.
            return self.func(*args)
        if args in self.cache:
            return self.cache[args]
        else:
            value = self.func(*args)
            self.cache[args] = value
            return value
    def __repr__(self):
        '''Return the function's docstring.'''
        return self.func.__doc__
    def __get__(self, obj, objtype):
        '''Support instance methods.'''
        return functools.partial(self.__call__, obj)
