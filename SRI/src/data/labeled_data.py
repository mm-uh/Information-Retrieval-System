from typing import List, Dict
from ..data.collection import Collection


class EvaluationDataSetIterator:
    def __init__(self, queries: List[str], relevant_indexes: Dict[int, List[int]]):
        self.__queries: List[str] = queries
        self.__relevant_indexes: Dict[int, List[int]] = relevant_indexes
        self.__index = -1
    
    def __next__(self) -> (str, List[int]):
        self.__index += 1
        if self.__index == len(self.__queries):
            raise StopIteration
        return (self.__queries[self.__index], self.__relevant_indexes[self.__index])
    

class EvaluationDataSet:
    def __init__(self, collection: Collection, queries: List[str], relvant_indexes: Dict[int, List[int]]):
        self.__collection: Collection = collection
        self.__queries: List[str] = queries
        self.__relevant_indexes: Dict[int, List[int]] = relvant_indexes
    
    def __iter__(self) -> EvaluationDataSetIterator:
        return EvaluationDataSetIterator(self.__queries, self.__relevant_indexes)

    @property
    def collection(self) -> Collection:
        return self.__collection

        
