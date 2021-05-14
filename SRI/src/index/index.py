from typing import List, Dict, Union
from ..logging import LoggerFactory
from ..utils.collection import Collection
from ..utils.processing_text import preprocess_data
from ..utils.utils import binary_search
from .posting import Posting


LOGGER = LoggerFactory('SRI').getChild('Indexer')


class Index:
    def __init__(self, collection: Collection):
        self.__index: Dict[str, List[Posting]] = {}
        self.__max_frequecy_in_document: Dict[int, int] = [0 for _ in range(len(collection))]
        LOGGER.info('Indexed started')
        for document_index, document in enumerate(collection):
            LOGGER.debug('Indexing document')
            self.__process_document(document_index, str(document))

    def __process_document(self, document_index: int, document: str):
        words: List[str] = preprocess_data(document)
        max_frequency:int = 0
        for word in words:
            LOGGER.debug(f'Updating word "{word}"" in index')
            frequency: int = self.__update_index_entry(document_index, word)
            max_frequency = max(max_frequency, frequency)
        self.__max_frequecy_in_document[document_index] = max_frequency

    def __update_index_entry(self, document_index: int, word: str) -> int:
        posting_list: List[Posting]
        try:
            posting_list = self.__index[word]
            last_posting: Posting = posting_list[-1]
            if last_posting.document_index == document_index:
                last_posting.increment_frequency()
                return last_posting.frequency
            else:
                posting_list.append(Posting(document_index))
                return 1
        except KeyError:
            LOGGER.debug('Creating new index entry')
            posting_list = [Posting(document_index)]
            self.__index[word] = posting_list
            return 1

    def get_posting_list(self, word: str) -> Posting:
        return self.__index[word]

    def get_number_of_documents_with_word(self, word: str) -> int:
        return len(self.__index[word])

    def get_posting(self, word: str, document_index: int) -> Union[None, Posting]:
        postings: List[Posting] = self.__index[word]
        document_indexes: List[int] = [p.document_index for p in postings]
        posting_index: int = binary_search(document_indexes, document_index)
        if posting_index == -1:
            return None
        return postings[posting_index]

    def get_most_repeated_word_in_document(self, document_index: int) -> int:
        return self.__max_frequecy_in_document[document_index]
    
    def filter_non_indexed_words(self, words: List[str]) -> List[str]:
        filtered_words: List[str] = []
        for word in words:
            try:
                _ = self.__index[word]
                filtered_words.append(word)
            except KeyError:
                continue
        return filtered_words
