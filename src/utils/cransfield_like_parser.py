from typing import List
from ..data.collection import Document
import re

SEPARATORS = ['.T', '.A', '.B', '.W', '.X']

class CransfieldLikeParser:
    def __init__(self):
        pass
    
    def parse(self, file):
        with open(file, 'r') as f:
            file_data = ''.join(f.readlines())
        documents: List[str] = re.split('.I \d', file_data)
        documents = list(map(lambda x : x.strip(), documents))
        documents = list(filter(lambda x : x!='', documents))
        return list(map(lambda x : self.__parse_document(x), documents))
    
    def __parse_document(self, document):
        document_lines: List[str] = document.split('\n')
        document_lines = list(map(lambda x: x.strip(), document_lines))
        available_separators: List[(int, str)] = []
        for sep in SEPARATORS:
            try:
                index: int = document_lines.index(sep)
                available_separators.append((index, sep))
            except ValueError:
                pass
        return self.__create_document(document_lines, available_separators)
        
    def __create_document(self, document_lines: List[str], sections):
        document: Document = Document()
        sections = sorted(sections)
        sections.append((len(document_lines), ''))
        for i, (index, header) in enumerate(sections):
            if header == '':
                break
            section_begin = index + 1
            section_end = sections[i+1][0]
            data = ''.join(document_lines[section_begin : section_end])
            if header == '.T':
                document.title = data
            elif header == '.A':
                document.author = data
            elif header == '.W':
                document.abstract = data
        return document
        
