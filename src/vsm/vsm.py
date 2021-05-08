from typing import List, Dict, TypeVar, Callable
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
    def __init__(self, collection: Collection, relevant_treshold: int = 10, alpha: float = 1, betha: float = 0.75):
        LOGGER.info("Initializing Model")
        self.__alpha = alpha
        self.__betha = betha
        self.__collection: Collection = collection
        LOGGER.info('Creating Index')
        self.__index: Index = Index(collection)
        self.__relevant_treshold: int = relevant_treshold
        LOGGER.info('Computing vectors for documents')
        self.__document_vectors: List[Vector] = [self.__create_document_vector(
            index) for index in range(len(self.__collection))]

    def query(self, query: str, relevants: List[int] = [], irrelevants: List[int] = []) -> List[int]:
        LOGGER.info(f"Querying {query}")
        scores: List[(float, int)] = []
        query_vector: Vector = self.__create_query_vector(query, relevants, irrelevants)
        for index in range(len(self.__collection)):
            score: float = self.__get_score(query_vector, index)
            scores.append((score, index))

        LOGGER.debug("Selecting best socores")
        sorted_scores: List[(float, int)] = sorted(scores, reverse=True)
        indexes = []
        for i in range(self.__relevant_treshold):
            indexes.append(sorted_scores[i][1])
        return indexes

    def __get_score(self, query_vector: Vector, document_index: int) -> float:
        LOGGER.debug("Computing score")
        document_vector: Vector = self.__document_vectors[document_index]
        document_vector = self.__normalize_vector(document_vector)
        # query_vector: Vector = self.__create_query_vector(query, relevants)
        return self.__compute_similarity(query_vector, document_vector)

    def __compute_similarity(self, vector1: Vector, vector2: Vector) -> float:
        return dot_product(vector1, vector2)

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

    def __create_query_vector(self, query: str, relevants: List[int], irrelevants: List[int]) -> Vector:
        LOGGER.debug("Creating query vector")

        query_words: List[str] = preprocess_data(query)
        query_words = self.__index.filter_non_indexed_words(query_words)
        frequencies: Counter = Counter(query_words)
        max_frequency = max(frequencies.values())
        alpha: float = 1 #if len(relevants) == 0 else self.__alpha
        query_vector = {word: self.__compute_query_weight(
            word, frequencies[word], max_frequency, alpha) for word in query_words}
        print(sum(query_vector.values()))
        relevant_weights = self.__compute_relevant_bias(relevants)
        irrelevants_weights = self.__compute_irrelevant_bias(irrelevants)
        result = vector_sum(query_vector, relevant_weights)
        print(sum(result.values()))
        result = vector_dif(result, irrelevants_weights)
        print(sum(result.values()))
        return result         
    
    def __compute_relevant_bias(self, relevants: List[int]) -> Vector:
        relevant_documents = [self.__document_vectors[index] for index in relevants]
        relevant_weights = {}
        for rd in relevant_documents:
            relevant_weights = vector_sum(relevant_weights, rd)
        relevant_weights = apply_all_vector(relevant_weights, lambda x : x/len(relevant_weights))
        relevant_weights = apply_all_vector(relevant_weights, lambda x : x*0.9)
        return relevant_weights
    
    def __compute_irrelevant_bias(self, irrelevants: List[int]) -> Vector:
        irrelevants_documents = [self.__document_vectors[index] for index in irrelevants]
        irrelevants_weights = {}
        for nr in irrelevants_documents:
            irrelevants_weights = vector_sum(irrelevants_weights, nr)
        irrelevants_weights = apply_all_vector(irrelevants_weights, lambda x : x/len(irrelevants_documents))
        irrelevants_weights = apply_all_vector(irrelevants_weights, lambda x : x*0.3)
        return irrelevants_weights

    def __compute_query_weight(self, word: str, frequency: float, max_frequency: float, alpha: float) -> float:
        tf: float = (SMOOTH_VALUE + (1 - SMOOTH_VALUE)
                     * frequency) / max_frequency
        idf: float = self.__get_idf(word)
        return tf * idf * alpha

    def __create_document_vector(self, document_index: int) -> Vector:
        LOGGER.debug("Creating document vector")
        document: Document = self.__collection[document_index]
        LOGGER.debug('Preprocessing document')
        document_words: List[str] = preprocess_data(str(document))
        return {word: self.__get_weight(
            word, document_index) for word in document_words}


def save_model(model, filename):
    LOGGER.info(f'Saving model to file {filename}')
    pickle.dump(model, open(filename, 'wb'))


def load_model(filename):
    LOGGER.info(f'Loading model from file {filename}')
    return pickle.load(open(filename, 'rb'))


def vector_sum(vector1: Vector, vector2: Vector) -> Vector:
    result: Vector = {}
    for key, value in vector1.items():
        try:
            result[key] += value
        except KeyError:
            result[key] = value
    for key, value in vector2.items():
        try:
            result[key] += value
        except KeyError:
            result[key] = value
    return result

def vector_dif(vector1: Vector, vector2: Vector) -> Vector:
    result: Vector = {}
    for key, value in vector1.items():
        try:
            result[key] = value - vector2[key]
        except KeyError:
            result[key] = value
    return result

def dot_product(vector1: Vector, vector2: Vector) -> float:
    similarity: float = 0.0
    for word, weight1 in vector1.items():
        try:
            weight2: float = vector2[word]
            similarity += weight1 * weight2
        except KeyError:
            continue
    return similarity

def apply_all_vector(vector: Vector, f: Callable[[float], float]) -> Vector:
    result: Vector = {}
    for key, value in vector.items():
        result[key] = f(value)
    return result
