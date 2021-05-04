from src.utils.cranfield_utils import read_query_file, read_documents
from src.utils.processing_text import tokenize_text, preprocess_data
from src.logging.logging import LoggerFactory
from src.index.index import Index
import logging

QUERY_FILE_PATH = 'cran.qry'
DOCUMENT_FILE_PATH = 'cran.all.1400'

LOGGER = LoggerFactory('SRI')
LOGGER.setLevel(logging.INFO)


def main():
    documents = read_documents(DOCUMENT_FILE_PATH)

    index = Index(documents)


if __name__ == '__main__':
    main()
