from typing import List, Dict, Callable, Set
from abc import ABC, abstractmethod
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


class Evaluator(ABC):
    @abstractmethod
    def evaluate(self):
        pass

    @abstractmethod
    def get_metrics(self):
        pass
class SimpleEvaluator(Evaluator):
    def __init__(self, dataset: EvaluationDataSet, model: VectorSpaceModel, metrics=['recall', 'precission', 'f1score']):
        LOGGER.info('Initializing evaluator')
        self.__dataset: EvaluationDataSet = dataset
        self.__model: VectorSpaceModel = model
        self.__metrics: Dict[str, List[float]] = {
            metric: [] for metric in metrics}

    def evaluate(self):
        LOGGER.info('Start evaluation')
        for query, relevant_indexes in self.__dataset:
            model_result: List[int] = self.__model.query(str(query))
            for metric, values in self.__metrics.items():
                metric_function: Callable[[
                    List[int], List[int]], float] = METRICS_FUNCTIONS[metric]
                values.append(metric_function(relevant_indexes, model_result))
        LOGGER.info('Evaluation ended')

    def get_metrics(self):
        return {metric: average(values) for metric, values in self.__metrics.items()}

class FeedbackEvaluator(Evaluator):
    def __init__(self, dataset: EvaluationDataSet, model: VectorSpaceModel, metrics=['recall', 'precission', 'f1score']):
        LOGGER.info('Initializing evaluator')
        self.__dataset: EvaluationDataSet = dataset
        self.__model: VectorSpaceModel = model
        self.__metrics: Dict[str, List[float]] = {
            metric: [] for metric in metrics}

    
    def evaluate(self):
        LOGGER.info('Start evaluation')
        for query, relevant_indexes in self.__dataset:
            model_result: List[int] = self.__model.query(str(query))
            rr, nr = self.__get_relevants_and_irrelevants(model_result, relevant_indexes)
            model_result = self.__model.query(str(query), rr, nr)
            for metric, values in self.__metrics.items():
                metric_function: Callable[[
                    List[int], List[int]], float] = METRICS_FUNCTIONS[metric]
                values.append(metric_function(relevant_indexes, model_result))

    def get_metrics(self):
        return {metric: average(values) for metric, values in self.__metrics.items()}
    
    def __get_relevants_and_irrelevants(self, a: List[int], b:List[int]) -> (List[int], List[int]):
        a: Set[int] = set(a)
        b: Set[int] = set(b)
        rr: Set[int] = a.intersection(b)
        nr: Set[int] = a.difference(b)
        return (list(rr), list(nr))
        
