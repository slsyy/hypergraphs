import uuid
from enum import Enum

import networkx as nx
from PIL.Image import Image

from utils import get_node_id

def P5(graph: nx.Graph, hyperedge_id, image: Image):
    check_condition(graph, hyperedge_id)
    graph.node[hyperedge_id]['should_break'] = 1
    P6(graph, hyperedge_id, image)

def check_conditions(graph, hyperedge_id):
    if not graph.node[hyperedge_id]['is_hyperedge']:
        raise ValueError('Given node_id is not id of hyperedge')
    if graph.node[hyperedge_id]['label'] is not 'I':
        raise ValueError('Given hyperedge label is not I')
    elif graph.node[hyperedge_id]['should_break'] is not 0:
        raise ValueError('Hyper edge has should_break set to 1, when it is supposed to be equal 0')
