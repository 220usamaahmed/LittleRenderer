from typing import Tuple, List
import math


def get_scallar_multiple(v: Tuple[float, ...], s: float):
    return tuple([c * s for c in v])


def get_direction_vector(v0: Tuple[float, ...], v1: Tuple[float, ...]):
    if len(v0) == len(v1):
        return tuple([v1[i] - v0[i] for i in range(len(v0))])
    else: raise Exception('The two vectors need to be of the same size')


def get_dot_product(v0: Tuple[float, ...], v1: Tuple[float, ...]):
    if len(v0) == len(v1):
        return sum([v1[i] * v0[i] for i in range(len(v0))])
    else: raise Exception('The two vectors need to be of the same size')


def get_cross_product(v0: Tuple[float, float, float],
    v1: Tuple[float, float, float]):
    if len(v0) == len(v1) == 3:
        return (
            v0[1] * v1[2] - v0[2] * v1[1],
            v0[2] * v1[0] - v0[0] * v1[2],
            v0[0] * v1[1] - v0[1] * v1[0]
        )
    else: raise Exception('The two vectors need to be of size 3')


def get_magnitude(v: Tuple[float, ...]):
    return math.sqrt(sum([c**2 for c in v]))


def normalize(v: Tuple[float, ...]):
    mag = get_magnitude(v)
    if mag == 0: return v
    else: return get_scallar_multiple(v, 1 / mag)


def get_bounding_box(vs: List[Tuple[float, ...]]):
    if len(vs) < 1:
        raise Exception('Need to pass atleast one vector')

    if len(set([len(v) for v in vs])) !=  1:
        raise Exception('The vectors need to be of the same size')

    box = []
    for c in range(len(vs[0])):
        box.append((
            vs[vs.index(min(vs, key=lambda x: x[c]))][c],
            vs[vs.index(max(vs, key=lambda x: x[c]))][c]
        ))
    return box
