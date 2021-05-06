from typing import List, Dict
from ..logging import LoggerFactory
from ..data.collection import Collection, Document
from collections import defaultdict

LOOGER = LoggerFactory('SRI').getChild('CranfieldTools')



def read_query_file(file: str) -> Collection: 
    with open(file, 'r') as f:
        all_queries_str: str = ''.join(f.readlines())
    queries: List[str] = __get_queries(all_queries_str)
    queries = list(map(__parse_query, queries))
    return Collection(queries)


def __get_queries(all_queries_str: str) -> List[str]:
    return list(filter(lambda x : x != '', all_queries_str.split('.I')))

def __parse_query(query: str) -> str:
    query_lines: List[str] = query.split('\n')
    text_begin: int = query_lines.index('.W') + 1
    query_text: str = ' '.join(query_lines[text_begin : ])
    return query_text

def read_documents(file: str) -> Collection:
    LOOGER.info(f'Parsing documents on file {file}')
    with open(file, 'r') as f:
        all_documents_str: str = ''.join(f.readlines())
    documents: List[str] = __get_documents(all_documents_str)
    documents: List[Document] = list(map(__parse_document, documents))
    return Collection(documents)

def __get_documents(all_documents_str: str) -> List[str]:
    return list(filter(lambda x : x != '', all_documents_str.split('.I')))

def __parse_document(document: str) -> Document:
    text_lines: List[str] = document.split('\n') 
    title_begin: int = text_lines.index('.T') + 1
    author_begin: int = text_lines.index('.A') + 1
    b_begin: int = text_lines.index('.B') + 1
    text_begin: int = text_lines.index('.W') + 1

    title: str = ' '.join(text_lines[title_begin : author_begin - 1])
    author: str = ' '.join(text_lines[author_begin : b_begin - 1])
    text: str = ' '.join(text_lines[text_begin : ])

    return Document(author, title, text)


def get_queries_document_relation(file: str, treshold: int) -> Dict[int, List[int]]:
    relations: Dict[int, List[int]] = defaultdict(lambda : list())
    with open(file, 'r') as f:
        for line in f.readlines():
            query, document, relation = map(int, line.split())
            if relation <= treshold:
                relations[query - 1].append(document - 1)
    return relations

