from typing import List
from ..index.index import Index
from ..utils.collection import Document, Collection
from ..utils.processing_text import preprocess_data


class VectorSpaceModel:
    def __init__(self, collection: Collection, relevant_treshold: int = 10):
        self.__collection: Collection = collection
        self.__index: Index = Index(collection)
        self.__relevant_treshold: int = relevant_treshold
    
    def query(self, query: str) -> List[Document]:
        pass
    
    def __get_score(self, query: str, document: Document) -> float:
        query_words: List[str] = preprocess_data(query)

    def __get_idf(self, word: str) -> float:
        documents_count: int = len(self.__collection)
        pass
    
    def __get_normalized_document_vector(self, document: Document):
        pass

    def __create_query_vector(self, query):
        pass