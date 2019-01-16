from typing import Dict, List, Tuple

from PIL import Image
from networkx import Graph

from hypergraphs.utils import get_node_data

COLORING_COEFFICIENT_CALCULATORS = {
    # corner number : function to calculate color coefficient
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
    matrices = create_matrices(max_x, max_y)
    was_pixel_approximated = {x: {y: False for y in range(max_y)} for x in range(max_x)}
    hyperedges_neighbors = find_hyperedges_neighbors(graph)
    for hyperedge_neighbors in sorted(hyperedges_neighbors, key=lambda neighbors: calculate_area(neighbors),
                                      reverse=True):
        x1, x2, y1, y2 = get_coordinates_from_neighbors(hyperedge_neighbors)
        corners_with_ids = enumerate_hyperedge_corners(graph, x1, x2, y1, y2, matrices)
        for px in range(x1, x2 + 1):
            for py in range(y1, y2 + 1):
                if not was_pixel_approximated[px][py]:
                    for corner_id, corner_data in corners_with_ids:
                        for matrix, color in zip(matrices, get_colors(corner_data)):
                            matrix[px][py] += calculate_color(color, corner_id, px, x1, x2, py, y1, y2)
                    was_pixel_approximated[px][py] = True
    return matrices


def create_matrices(max_x: int, max_y: int) -> Tuple[Dict, Dict, Dict]:
    approx_r = create_approximation_matrix(max_x, max_y)
    approx_g = create_approximation_matrix(max_x, max_y)
    approx_b = create_approximation_matrix(max_x, max_y)
    return approx_r, approx_g, approx_b


def create_approximation_matrix(max_x: int, max_y: int) -> Dict[int, Dict[int, float]]:
    return {x: {y: 0.0 for y in range(max_y)} for x in range(max_x)}


def find_hyperedges_neighbors(graph: Graph) -> List[List[Dict]]:
    return [get_node_neighbors_data(graph, node_id) for node_id, node_data in graph.nodes(data=True)
            if is_hyperedge_I(node_data)]


def get_node_neighbors_data(graph: Graph, node_id: int) -> List[Dict]:
    return [graph.node[neighbor_id] for neighbor_id in graph.neighbors(node_id)]


def is_hyperedge_I(node_data: Dict) -> bool:
    return node_data['is_hyperedge'] and node_data['label'] == 'I'


def calculate_area(hyperedge_neighbors_data: List[Dict]) -> int:
    x1, x2, y1, y2 = get_coordinates_from_neighbors(hyperedge_neighbors_data)
    return (x2 - x1) * (y2 - y1)


def get_coordinates_from_neighbors(neighbors_data: List[Dict]) -> Tuple[int, int, int, int]:
    xs, ys = set(), set()
    for neighbor_data in neighbors_data:
        xs.add(neighbor_data['x'])
        ys.add(neighbor_data['y'])
    return min(xs), max(xs), min(ys), max(ys)


def enumerate_hyperedge_corners(graph: Graph, x1: int, x2: int, y1: int, y2: int, matrices: Tuple[Dict, Dict, Dict]) \
        -> List[Tuple[int, Dict]]:
    return [(get_corner_number(corner_data, x1, x2, y1, y2), corner_data)
            for corner_data in get_corners_data(graph, x1, x2, y1, y2, matrices)]


def get_corner_number(corner_data: Dict, x1: int, x2: int, y1: int, y2: int) -> int:
    x, y = corner_data['x'], corner_data['y']
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


def get_corners_data(graph: Graph, x1: int, x2: int, y1: int, y2: int, matrices: Tuple[Dict, Dict, Dict]) -> List[Dict]:
    corners_data = []
    for x in (x1, x2):
        for y in (y1, y2):
            try:
                corners_data.append(get_node_data(graph, (x, y)))
            except KeyError:
                corners_data.append(
                    {'x': x, 'y': y, 'r': matrices[0][x][y], 'g': matrices[1][x][y], 'b': matrices[2][x][y]})
    return corners_data


def get_colors(node_data: Dict) -> Tuple[float, float, float]:
    return node_data['r'], node_data['g'], node_data['b']


def calculate_color(color: float, corner_number: int, px: int, x1: int, x2: int, py: int, y1: int, y2: int) -> float:
    return color * COLORING_COEFFICIENT_CALCULATORS[corner_number](px, x1, x2, py, y1, y2)


def draw_approximation(image: Image, approx_r: Dict, approx_g: Dict, approx_b: Dict):
    # if the image is not showing refer to this stackoverflow thread:
    # https://stackoverflow.com/questions/16279441/image-show-wont-display-the-picture
    bitmap = Image.new('RGB', image.size)
    pixels = bitmap.load()
    for x in range(image.width):
        for y in range(image.height):
            pixels[x, y] = (round(approx_r[x][y]), round(approx_g[x][y]), round(approx_b[x][y]))
    bitmap.show()
