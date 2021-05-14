from typing import List, Set


def compute_precission(real: List[int], pred: List[int]) -> float:
    if len(pred) == 0:
        return 0

    real: Set[int] = set(real)
    pred: Set[int] = set(pred)

    rr: Set[int] = real.intersection(pred)
    ri: Set[int] = pred.difference(real)

    return len(rr) / (len(rr) + len(ri))


def compute_recall(real, pred) -> float:
    if len(real) == 0:
        return 0

    real: Set[int] = set(real)
    pred: Set[int] = set(pred)

    rr: Set[int] = real.intersection(pred)
    nr: Set[int] = real.difference(pred)

    return len(rr) / (len(rr) + len(nr))


def compute_f1score(real: List[int], pred: List[int]) -> float:
    p: float = compute_precission(real, pred)
    r: float = compute_recall(real, pred)

    if p == r == 0:
        return 0
    
    return 2*p*r / (p + r)