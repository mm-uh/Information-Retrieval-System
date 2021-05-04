from typing import List

class Collection:
    def __init__(self, documents: List[str]):
        self.documents = documents
    
    def __getitem__ (self, index) -> str:
        return self.documents[index]
    
    def __len__(self) -> int:
        return len(self.documents)