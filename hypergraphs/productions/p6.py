import uuid
from enum import Enum

import networkx as nx
from PIL.Image import Image

from utils import get_node_id, get_common_nodes, get_f1_nodes, get_f2_nodes, get_i_nodes, common_elements

def P6(graph: nx.Graph, hyperedge_id, image: Image):
    check_conditions(graph, hyperedge_id)

    #Find bigger neighbours procedure
    #First of all: find common nodes connected with our hyperedge
    for common_node_a in get_common_nodes(graph, hyperedge_id):
        #Second thing: find F1 and F2 hyperedges connected with common node
        for f_hyperedge in get_f1_nodes(graph, common_node_a) + get_f2_nodes(graph, common_node_a):
            #Third: find other common nodes for F* hyperedges
            f_hyperedge_common_nodes = get_common_nodes(graph, f_hyperedge)
            #Make sure that our hyperedges have at least two common nodes
            if len(f_hyperedge_common_nodes) < 2:
                continue
            common_node_b = list(filter(lambda cn: cn != common_node_a, f_hyperedge_common_nodes))[0]
            #Fourth: find all 'I' hyperedges between common_node_a and common_node_b
            i_hyperedges = common_elements(get_i_nodes(graph, common_node_a), get_i_nodes(graph, common_node_b))
            #If i_hyperedges contains our hyperedge, it means that our neighbour is not bigger than we
            #If it doesn't contain our hyperedge, it means that we should set him should_break flag
            if hyperedge_id not in i_hyperedges:
                for i_hyperedge in i_hyperedges:
                    graph.node[i_hyperedge]['should_break'] = 1
                    P6(graph, i_hyperedge, image)

def check_conditions(graph, hyperedge_id):
    if not graph.node[hyperedge_id]['is_hyperedge']:
        raise ValueError('Given node_id is not id of hyperedge')
    if graph.node[hyperedge_id]['label'] is not 'I':
        raise ValueError('Given hyperedge label is not I')
    elif graph.node[hyperedge_id]['should_break'] is 0:
        raise ValueError('Hyper edge has should_break set to 0, when it is supposed to be equal 1')
