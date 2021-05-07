from typing import List, Dict, Callable
from .metrics import compute_f1score, compute_precission, compute_recall
from ..data.labeled_data import EvaluationDataSet
from ..vsm.vsm import VectorSpaceModel
from ..utils.utils import average
from ..logging.logging import LoggerFactory


LOGGER = LoggerFactory('SRI').getChild('Evaluator')

METRICS_FUNCTIONS = {
    'recall': compute_recall,
    'precission': compute_precission,
    'f1score': compute_f1score
}


class Evaluator:
    def __init__(self, dataset: EvaluationDataSet, model: VectorSpaceModel, metrics=['recall', 'precission', 'f1score']):
        LOGGER.info('Initializing evaluator')
        self.__dataset: EvaluationDataSet = dataset
        self.__model: VectorSpaceModel = model
        self.__metrics: Dict[str, List[float]] = {
            metric: [] for metric in metrics}

    def evaluate(self):
        LOGGER.info('Start evaluation')
        for query, relevant_indexes in self.__dataset:
            model_result: List[int] = self.__model.query(query)
            for metric, values in self.__metrics.items():
                metric_function: Callable[[
                    List[int], List[int]], float] = METRICS_FUNCTIONS[metric]
                values.append(metric_function(relevant_indexes, model_result))
        LOGGER.info('Evaluation ended')

    def get_metrics(self):
        return {metric: average(values) for metric, values in self.__metrics.items()}
