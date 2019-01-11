import os
from enum import Enum
from typing import Dict, Tuple

from networkx import Graph

IMAGE_PATH = os.path.join(os.path.dirname(__file__), "tests/test_data", "four_colors.jpg")


class HyperEdge(Enum):
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


def get_node_data(graph: Graph, node_position: Tuple[int, int]) -> Dict:
    """
    :param graph:
    :param node_position: a tuple containing x and y coordinates of a node
    :return: node data
    """
    return graph.node[get_node_id(node_position)]


def convert_to_hex(rgba: Tuple[int, int, int, int]) -> str:
    return '#%02x%02x%02x' % rgba[:3]


def get_common_nodes(graph, hyperedge_id):
    if not graph.node[hyperedge_id]['is_hyperedge']:
        raise ValueError('Given node_id is not id of hyperedge')
    return [common_node for common_node in graph[hyperedge_id]]


def get_f1_nodes(graph, common_node_id):
    return __get_x_nodes(graph, common_node_id, Direction.N) + \
           __get_x_nodes(graph, common_node_id, Direction.S)


def get_f2_nodes(graph, common_node_id):
    return __get_x_nodes(graph, common_node_id, Direction.W) + \
           __get_x_nodes(graph, common_node_id, Direction.E)


def get_i_nodes(graph, common_node_id):
    return __get_x_nodes(graph, common_node_id, HyperEdge.I)


def __get_x_nodes(graph, common_node_id, label):
    if graph.node[common_node_id]['is_hyperedge']:
        raise ValueError('Given node_id is not id of common node')
    return [x_node for x_node in graph[common_node_id] if graph.nodes[x_node]['label'] == label.name]


def common_elements(list1, list2):
    return list(set(list1).intersection(list2))
