from typing import Tuple


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
    if graph.node[hyperedge_id]['is_hyperedge']:
        raise ValueError('Given node_id is not id of common node')
    return [f1_node for f1_node in graph[common_node_id] if graph.nodes[f1_node]['label'] == 'F1']

def get_f2_nodes(graph, common_node_id):
    if graph.node[hyperedge_id]['is_hyperedge']:
        raise ValueError('Given node_id is not id of common node')
    return [f2_node for f2_node in graph[common_node_id] if graph.nodes[f1_node]['label'] == 'F2']

def get_i_nodes(graph, common_node_id):
    if graph.node[hyperedge_id]['is_hyperedge']:
        raise ValueError('Given node_id is not id of common node')
    return [i_node for i_node in graph[common_node_id] if graph.nodes[f1_node]['label'] == 'I']

def common_elements(list1, list2):
    return list(set(list1).intersection(list2))
