from typing import Tuple, Dict, List

from networkx import Graph

NEIGHBOR_COLORING_COEFFICIENTS_CALCULATORS = {
    # neighbor_number : function to calculate color coefficient
    1: lambda px, x1, x2, py, y1, y2: (1 - (px - x1) / (x2 - x1)) * ((py - y1) / (y2 - y1)),
    2: lambda px, x1, x2, py, y1, y2: ((px - x1) / (x2 - x1)) * ((py - y1) / (y2 - y1)),
    3: lambda px, x1, x2, py, y1, y2: (1 - (px - x1) / (x2 - x1)) * (1 - (py - y1) / (y2 - y1)),
    4: lambda px, x1, x2, py, y1, y2: ((px - x1) / (x2 - x1)) * (1 - (py - y1) / (y2 - y1))
}


def approximate(graph: Graph, max_x: int, max_y: int) -> Tuple[Dict, Dict, Dict]:
    """
    Calculates matrices that approximate image bitmap
    :param graph: hypergraph representing bitmap
    :param max_x: image x axis size (width)
    :param max_y: image y axis size (height)
    :return: returns matrices that approximate bitmap colors
    """
    APPROX_R = create_approximation_matrix(max_x, max_y)
    APPROX_G = create_approximation_matrix(max_x, max_y)
    APPROX_B = create_approximation_matrix(max_x, max_y)
    matrices = (APPROX_R, APPROX_G, APPROX_B)
    for node_id, node_data in graph.nodes(data=True):
        if is_hyperedge_I(node_data):
            neighbors_data = get_node_neighbors_data(graph, node_id)
            x1, x2, y1, y2 = get_coordinates_from_neighbors(neighbors_data)
            for neighbor_data in neighbors_data:
                neighbor_number = get_neighbor_number(neighbor_data, x1, x2, y1, y2)
                neighbor_colors = get_colors(neighbor_data)
                for px in (x1, x2):
                    for py in (y1, y2):
                        for matrix, color in zip(matrices, neighbor_colors):
                            matrix[px][py] += calculate_color(color, neighbor_number, px, x1, x2, py, y1, y2)
    return matrices


def create_approximation_matrix(max_x: int, max_y: int) -> Dict[int, Dict[int, float]]:
    approximation_matrix = {}
    for x in range(max_x):
        approximation_matrix[x] = {}
        for y in range(max_y):
            approximation_matrix[x][y] = 0.0
    return approximation_matrix


def is_hyperedge_I(node_data: Dict) -> bool:
    return node_data['is_hyperedge'] and node_data['label'] == 'I'


def get_node_neighbors_data(graph: Graph, node_id: int) -> List[Dict]:
    return list(graph.node[neighbor_id] for neighbor_id in graph.neighbors(node_id))


def get_coordinates_from_neighbors(neighbors_data: List[Dict]) -> Tuple[int, int, int, int]:
    xs, ys = set(), set()
    for neighbor_data in neighbors_data:
        xs.add(neighbor_data['x'])
        ys.add(neighbor_data['y'])
    return min(xs), max(xs), min(ys), max(ys)


def get_neighbor_number(neighbor_data: Dict, x1: int, x2: int, y1: int, y2: int) -> int:
    x, y = neighbor_data['x'], neighbor_data['y']
    if x == x1:
        if y == y2:
            return 1
        elif y == y1:
            return 3
    elif x == x2:
        if y == y2:
            return 2
        elif y == y1:
            return 4
    raise ValueError('Cannot identify neighbor number!')


def get_colors(node_data: Dict) -> Tuple[float, float, float]:
    return node_data['r'], node_data['g'], node_data['b']


def calculate_color(color: float, neighbor_number: int, px: int, x1: int, x2: int, py: int, y1: int, y2: int) -> float:
    return color * NEIGHBOR_COLORING_COEFFICIENTS_CALCULATORS[neighbor_number](px, x1, x2, py, y1, y2)
