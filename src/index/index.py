from typing import List, Dict
from ..utils.collection import Collection
from ..utils.processing_text import preprocess_data
from .posting import Posting

class Index:
    def __init__(self, collection: Collection):
        self.__index: Dict[str, List[Posting]]  = {}
        text: str
        for document_index, text in enumerate(collection):
            self.__process_document(document_index, text)
    
    def __process_document(self, document_index: int, document: str):
        words: List[str] = preprocess_data(document)
        for word in words:
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
            posting_list = [Posting(document_index)]
            self.__index[word] = posting_list

            