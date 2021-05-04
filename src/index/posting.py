
class Posting:
    def __init__(self, document_index: int):
        self.__document_index: int = document_index
        self.__term_frequency: int = 0
    
    def __eq__(self, other: Posting):
        return self.__document_index == other.document_index
    
    def increment_frequency(self, amount: int = 1):
        self.__term_frequency += amount
    
    @property
    def document_index(self) -> int:
        return self.__document_index
    
    @property
    def frequency(self) -> int:
        return self.__term_frequency