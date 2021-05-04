from src.utils.cranfield_utils import read_query_file, read_documents
from src.utils.processing_text import tokenize_text, preprocess_data

QUERY_FILE_PATH = 'cran.qry'
DOCUMENT_FILE_PATH = 'cran.all.1400'


def main():
    first_document = read_documents(DOCUMENT_FILE_PATH)[0]
    first_document_str = str(first_document)
    print(first_document_str)
    print()
    print(tokenize_text(first_document_str))
    print()
    print(preprocess_data(first_document_str))


if __name__ == '__main__':
    main()
