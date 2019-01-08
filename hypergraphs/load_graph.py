from productions import P1, P2
from typing import TextIO, Tuple
from types import SimpleNamespace
from unittest.mock import Mock

import networkx as nx


def load_graph(file: TextIO) -> nx.Graph:
    graph = nx.Graph()

    for prod_sign in __read_production(file):
        __execute_production(graph, prod_sign)

    return graph


def __read_production(stream: TextIO) -> Tuple:
    prod_num = int(stream.readline())
    attributes = stream.readline().split(',')

    if not prod_num or not attributes:
        raise StopIteration

    if not prod_num in range(1, 6):
        raise ValueError('Invalid production number: {}'.format(prod_num))

    yield prod_num, map(lambda arg: int(arg), attributes)


def __execute_production(graph: nx.Graph, prod_sign: Tuple):
    # P1 only for now
    if prod_sign[0] == 1:
        x_max, y_max, r1, g1, b1, r2, g2, b2, r3, g3, b3, r4, g4, b4 = prod_sign[1]

        def sample(x, y):
            if (x, y) == (0, y_max):
                return r1, g1, b1
            elif (x, y) == (x_max, y_max):
                return r2, g2, b2
            elif (x, y) == (0, 0):
                return r3, g3, b3
            elif (x, y) == (x_max, 0):
                return r4, g4, b4

        image = SimpleNamespace()
        image.readpixel = Mock(side_effect=sample)

        P1(graph, x_max, y_max, image)
