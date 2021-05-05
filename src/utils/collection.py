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
        self.__index: int
    
    def __next__(self) -> str:
        if self.__index == len(self.__collection): 
            raise StopIteration
        self.__index += 1
        return self.__collection[self.__index]


class Document:
    def __init__(self, author: str, title: str, text: str):
        self.author = author
        self.title = title
        self.text = text
    
    def __repr__(self) -> str:
        return self.text

