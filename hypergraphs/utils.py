from enum import Enum
from typing import Tuple


class HyperEdge(Enum):
    F1 = 'F1'
    F2 = 'F2'
    I = 'I'
    B = 'B'


class Direction(Enum):
    N = 1
    S = 2
    W = 3
    E = 4


def get_node_id(node_position: Tuple[int, int]) -> int:
    """
    :param node_position: a tuple containing x and y coordinates of a node
    :return: node id, a hash of node position
    """
    return hash(node_position)


def convert_to_hex(rgba: Tuple[int, int, int, int]) -> str:
    return '#%02x%02x%02x' % rgba[:3]


def get_common_nodes(graph, hyperedge_id):
    if not graph.node[hyperedge_id]['is_hyperedge']:
        raise ValueError('Given node_id is not id of hyperedge')
    return [common_node for common_node in graph[hyperedge_id]]


def get_f1_nodes(graph, common_node_id):
    allnodes =  [ data for idd, data in graph.nodes(data=True)]
    tmpnodes = __get_x_nodes(graph, common_node_id, Direction.S)
    tmp2nodes = __get_x_nodes(graph, common_node_id, Direction.N)
    nodes = __get_x_nodes(graph, common_node_id, HyperEdge.F1)
    return __get_x_nodes(graph, common_node_id, HyperEdge.F1)


def get_f2_nodes(graph, common_node_id):
    allnodes = [ data for idd, data in graph.nodes(data=True)]
    tmpnodes = __get_x_nodes(graph, common_node_id, Direction.W)
    tmp2nodes = __get_x_nodes(graph, common_node_id, Direction.E)
    nodes = __get_x_nodes(graph, common_node_id, HyperEdge.F2)
    return __get_x_nodes(graph, common_node_id, HyperEdge.F2)


def get_i_nodes(graph, common_node_id):
    nodes = __get_x_nodes(graph, common_node_id, HyperEdge.I.name)
    return __get_x_nodes(graph, common_node_id, HyperEdge.I.name)


def __get_x_nodes(graph, common_node_id, label):
    if graph.node[common_node_id]['is_hyperedge']:
        raise ValueError('Given node_id is not id of common node')
    return [x_node for x_node in graph[common_node_id] if graph.nodes[x_node]['label'] == label]


def common_elements(list1, list2):
    return list(set(list1).intersection(list2))
