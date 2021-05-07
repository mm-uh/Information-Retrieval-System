from typing import List, Dict
from collections import defaultdict
from ..data.collection import Document
import re

SEPARATORS = ['.T', '.A', '.B', '.W', '.X']


class CransfieldLikeParser:
    @staticmethod
    def parse(file):
        with open(file, 'r') as f:
            file_data = ''.join(f.readlines())
        documents: List[str] = re.split('.I \d', file_data)
        documents = [document_str.strip() for document_str in documents]
        documents = [document_str for document_str in documents if not document_str == '']
        return [CransfieldLikeParser.__parse_document(document) for document in documents]

    @staticmethod
    def __parse_document(document):
        document_lines: List[str] = document.split('\n')
        document_lines = list(map(lambda x: x.strip(), document_lines))
        available_separators: List[(int, str)] = []
        for sep in SEPARATORS:
            try:
                index: int = document_lines.index(sep)
                available_separators.append((index, sep))
            except ValueError:
                pass
        return CransfieldLikeParser.__create_document(document_lines, available_separators)

    @staticmethod
    def __create_document(document_lines: List[str], sections):
        document: Document = Document()
        sections = sorted(sections)
        sections.append((len(document_lines), ''))
        for i, (index, header) in enumerate(sections):
            if header == '':
                break
            section_begin = index + 1
            section_end = sections[i+1][0]
            data = ''.join(document_lines[section_begin: section_end])
            if header == '.T':
                document.title = data
            elif header == '.A':
                document.author = data
            elif header == '.W':
                document.abstract = data
        return document

    @staticmethod
    def parse_relevances(file, treshold=5):
        relations: Dict[int, List[int]] = defaultdict(lambda: list())
        with open(file, 'r') as f:
            for line in f.readlines():
                query, document, relation, * \
                    _ = map(lambda x: int(float(x)), line.split())
                if relation <= treshold:
                    relations[query - 1].append(document - 1)
        return relations
