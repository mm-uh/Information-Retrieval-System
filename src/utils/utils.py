from typing import List, TypeVar

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
        
        
        