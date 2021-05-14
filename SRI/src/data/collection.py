from typing import List


class Collection:
    def __init__(self, documents: List[str]):
        self.documents = documents
    
    def __getitem__ (self, index) -> str:
        return self.documents[index]
    
    def __len__(self) -> int:
        return len(self.documents)
    
    def __iter__(self) -> 'CollectionIterator':
        return CollectionIterator(self)
    

class CollectionIterator:
    def __init__(self, collection: Collection):
        self.__collection: Collection = collection
        self.__index: int = -1
    
    def __next__(self) -> str:
        self.__index += 1
        if self.__index == len(self.__collection): 
            raise StopIteration
        return self.__collection[self.__index]


class Document:
    def __init__(self):
        self.author: str = ''
        self.title: str = ''
        self.abstract: str = ''

    def __repr__(self) -> str:
        return f'{self.title}\n{self.abstract}\n{self.author}'
