from typing import List, Dict, TypeVar
from ..index.index import Index
from ..index.posting import Posting
from ..utils.collection import Document, Collection
from ..utils.processing_text import preprocess_data
from ..utils.utils import memoized
from ..logging.logging import LoggerFactory
from math import log10, sqrt
from collections import Counter
import pickle

LOGGER = LoggerFactory('SRI').getChild('VectorSpaceModel')
Vector = TypeVar('Vector')
SMOOTH_VALUE = 0.5


class VectorSpaceModel:
    def __init__(self, collection: Collection, relevant_treshold: int = 10):
        self.__collection: Collection = collection
        self.__index: Index = Index(collection)
        self.__relevant_treshold: int = relevant_treshold
        self.__document_vectors: List[Vector] = [self.__create_document_vector(
            index) for index in range(len(self.__collection))]

    def query(self, query: str) -> List[int]:
        LOGGER.debug("Querying {query}")
        scores: List[(float, int)] = []
        for index in range(len(self.__collection)):
            score: float = self.__get_score(query, index)
            scores.append((score, index))

        LOGGER.debug("Selecting best socores")
        sorted_scores: List[(float, int)] = sorted(scores, reverse=True)
        indexes = []
        for i in range(self.__relevant_treshold):
            indexes.append(sorted_scores[i][1])
        return indexes

    def __get_score(self, query: str, document_index: int) -> float:
        LOGGER.debug("Computing score")
        # document_vector: Vector = self.__create_document_vector(document_index)
        document_vector: Vector = self.__document_vectors[document_index]
        document_vector = self.__normalize_vector(document_vector)
        query_vector: Vector = self.__create_query_vector(query)
        return self.__compute_similarity(query_vector, document_vector)

    def __compute_similarity(self, vector1: Vector, vector2: Vector) -> float:
        similarity: float = 0.0
        for word, weight1 in vector1.items():
            try:
                weight2: float = vector2[word]
                similarity += weight1 * weight2
            except KeyError:
                continue
        return similarity

    def __get_weight(self, word: str, document_index: int) -> float:
        idf: float = self.__get_idf(word)
        tf: float = self.__get_tf(word, document_index)
        return idf * tf

    @memoized
    def __get_idf(self, word: str) -> float:
        LOGGER.debug('Computing idf')
        documents_count: int = len(self.__collection)
        documents_with_word: int = self.__index.get_number_of_documents_with_word(
            word)
        return log10(documents_count / documents_with_word)

    def __get_tf(self, word: str, document_index: int) -> float:
        LOGGER.debug('Computing tf')
        max_frequency = self.__index.get_most_repeated_word_in_document(
            document_index)
        posting: Posting = self.__index.get_posting(word, document_index)
        return posting.frequency / max_frequency

    def __normalize_vector(self, vector: Vector) -> Vector:
        weights: List[float] = list(vector.values())
        norm: float = sqrt(sum(map(lambda x: x**2, weights)))
        return {word: (weight / norm) for word, weight in vector.items()}

    def __create_query_vector(self, query: str) -> Vector:
        LOGGER.debug("Creating query vector")
        query_words: List[str] = preprocess_data(query)
        query_words = self.__index.filter_non_indexed_words(query_words)
        frequencies: Counter = Counter(query_words)
        max_frequency = max(frequencies.values())
        return {
            word: self.__compute_query_weight(word, frequencies[word], max_frequency) for word in query_words}

    def __compute_query_weight(self, word: str, frequency: float, max_frequency: float) -> float:
        tf: float = (SMOOTH_VALUE + (1 - SMOOTH_VALUE)
                     * frequency) / max_frequency
        idf: float = self.__get_idf(word)
        return tf * idf

    def __create_document_vector(self, document_index: int) -> Vector:
        LOGGER.debug("Creating document vector")
        document: Document = self.__collection[document_index]
        LOGGER.debug('Preprocessing document')
        document_words: List[str] = preprocess_data(str(document))
        return {word: self.__get_weight(
            word, document_index) for word in document_words}


def save_model(model, filename):
    pickle.dump(model, open(filename, 'wb'))

def load_model(filename):
    return pickle.load(open(filename, 'rb'))
