from src.utils.cransfield_like_parser import CransfieldLikeParser
from src.utils.processing_text import tokenize_text, preprocess_data
from src.logging.logging import LoggerFactory
from src.index.index import Index
from src.vsm.vsm import VectorSpaceModel, save_model, load_model
from src.data.labeled_data import EvaluationDataSet
from src.evaluator.evaluator import SimpleEvaluator, FeedbackEvaluator
from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import argparse

app = Flask(__name__)
CORS(app)

CRANS_CONSTANTS = ('datasets/cransfield/cran.qry', 'datasets/cransfield/cran.all.1400', 'datasets/cransfield/cranqrel', 'cransfield_model.vsm')
CISI_CONSTANTS = ('datasets/cisi/CISI.QRY', 'datasets/cisi/CISI.ALL', 'datasets/cisi/CISI.REL', 'cisi_model.vsm')
MED_CONSTANTS = ('datasets/med/MED.QRY', 'datasets/med/MED.ALL', 'datasets/med/MED.REL', 'med_model.vsm')
COLLECTIONS = {
    'Cransfield' : CRANS_CONSTANTS,
    'Medline' : MED_CONSTANTS,
    'Cisi' : CISI_CONSTANTS,
}

LOGGER = LoggerFactory('SRI')
LOGGER.setLevel(logging.INFO)

VSM = None


@app.route('/query', methods=['POST'])
def query():
    query = request.json['data']
    relevants = request.json['relevants']
    irrelevants = request.json['irrelevants']
    ranking = VSM.query(query, relevants, irrelevants)
    relevant_documents = [{'title': documents[index].title,
                           'abstract': documents[index].abstract[:250], 'index': index} for index in ranking]
    return jsonify(relevant_documents)


def main(parsed_args):
    collection = parsed_args.collection
    queries_file, documents_file, relations_file, model_file = COLLECTIONS[collection]
    global documents
    documents = CransfieldLikeParser.parse(documents_file)
    queries = CransfieldLikeParser.parse(queries_file)
    relations = CransfieldLikeParser.parse_relevances(relations_file)
    vsm = load_model(model_file)

    if parsed_args.evaluate:
        dataset = EvaluationDataSet(documents, queries, relations)
        evaluator = SimpleEvaluator(dataset, vsm)
        evaluator.evaluate()
        metrics = evaluator.get_metrics()
        for metric, value in metrics.items():
            print(metric + ': ' + str(value))
    else:
        global VSM
        VSM = vsm
        app.run(debug=False)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Sistema de Recuperación de Información')
    parser.add_argument('-e', action='store_const', help='Just evaluate over collection', const=True, dest='evaluate')
    parser.add_argument('-c', action='store', help='Select the collection to use Cransfield, Medline or Cisi', default='Cransfield', dest='collection')
    result = parser.parse_args()
    main(result)
