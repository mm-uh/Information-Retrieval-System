from typing import List, Dict
from ..logging import LoggerFactory
from ..utils.collection import Collection
from ..utils.processing_text import preprocess_data
from .posting import Posting


LOGGER = LoggerFactory('SRI').getChild('Indexer')

class Index:
    def __init__(self, collection: Collection):
        self.__index: Dict[str, List[Posting]]  = {}
        text: str
        LOGGER.info('Indexed started')
        for document_index, document in enumerate(collection):
            LOGGER.debug('Indexing document')
            self.__process_document(document_index, str(document))
    
    def __process_document(self, document_index: int, document: str):
        words: List[str] = preprocess_data(document)
        for word in words:
            LOGGER.debug(f'Updating word: {word} in index')
            self.__update_index_entry(document_index, word)
    
    def __update_index_entry(self, document_index: int, word: str):
        posting_list: List[Posting]
        try:
            posting_list = self.__index[word]
            last_posting: Posting = posting_list[-1]
            if last_posting.document_index == document_index:
                last_posting.increment_frequency()
            else:
                posting_list.append(Posting(document_index))
        except KeyError:
            LOGGER.debug('Creating new index entry')
            posting_list = [Posting(document_index)]
            self.__index[word] = posting_list

            