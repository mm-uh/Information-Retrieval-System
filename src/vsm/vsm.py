from typing import List, Dict, TypeVar
from ..index.index import Index
from ..index.posting import Posting
from ..utils.collection import Document, Collection
from ..utils.processing_text import preprocess_data
from math import log10, sqrt

Vector = TypeVar('Vector')


class VectorSpaceModel:
    def __init__(self, collection: Collection, relevant_treshold: int = 10):
        self.__collection: Collection = collection
        self.__index: Index = Index(collection)
        self.__relevant_treshold: int = relevant_treshold

    def query(self, query: str) -> List[Document]:
        pass

    def __get_score(self, query: str, document_index: int) -> float:
        document_vector: Vector = self.__create_document_vector(document_index)
        document_vector = self.__normalize_vector(document_vector)

    def __get_weight(self, word: str, document_index: int) -> float:
        idf: float = self.__get_idf(word)
        tf: float = self.__get_tf(word, document_index)
        return idf * tf

    def __get_idf(self, word: str) -> float:
        documents_count: int = len(self.__collection)
        documents_with_word: int = self.__index.get_number_of_documents_with_word(
            word)
        return log10(documents_count / documents_with_word)

    def __get_tf(self, word: str, document_index: int) -> float:
        _, max_frequency = self.__index.get_most_repeated_word_in_document(
            document_index)
        posting: Posting = self.__index.get_posting(word, document_index)
        return posting.frequency / max_frequency

    def __normalize_vector(self, vector: Vector) -> Vector:
        weights: List[float] = list(vector.values())
        norm: float = sqrt(sum(map(lambda x: x**2, weights)))
        return {word: (weight / norm) for word, weight in vector.items()}

    def __create_query_vector(self, query):
        pass

    def __create_document_vector(self, document_index: int) -> Vector:
        document: Document = self.__collection[document_index]
        document_words: List[str] = preprocess_data(str(document))
        return {word: self.__get_weight(
            word, document_index) for word in document_words}
