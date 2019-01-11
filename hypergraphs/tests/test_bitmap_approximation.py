from typing import Tuple, List
from unittest import TestCase
from uuid import uuid4, UUID

from PIL import Image
from networkx import Graph
from parameterized import parameterized

from hypergraphs.plot import plot
from hypergraphs.procedures.bitmap_approximation import approximate, draw_approximation
from hypergraphs.productions import P1
from hypergraphs.utils import get_node_id


class TestBitmapApproximation(TestCase):

    @parameterized.expand(['red', 'green', 'blue', 'white', 'black'])
    def test_coloring(self, color: str) -> None:
        # given:
        image = Image.new('RGB', (400, 400), color)
        image.show()
        # and
        graph = prepare_graph(image)

        # when:
        matrices = approximate(graph, image.width, image.height)
        draw_approximation(image, *matrices)

        # then:
        for x in range(image.width):
            for y in range(image.height):
                for image_color, color_matrix in zip(image.getpixel((x, y)), matrices):
                    self.assertAlmostEqual(image_color, color_matrix[x][y])


def prepare_graph(image: Image):
    graph = Graph()
    P1(graph, image.width // 2 - 1, image.height - 1, image)

    upper_right_node = image.width - 1, image.height - 1
    mid_right_node = image.width - 1, image.height // 2 - 1
    lower_right_node = image.width - 1, 0
    add_nodes(graph, image, [lower_right_node, mid_right_node, upper_right_node])

    upper_hyperedge = uuid4(), 3 * image.width // 4, 3 * image.height // 4
    lower_hyperedge = uuid4(), 3 * image.width // 4, image.height // 4
    add_hyperedges_nodes(graph, [upper_hyperedge, lower_hyperedge])

    upper_hyperedge_neighbors = [(image.width // 2 - 1, image.height - 1), upper_right_node, mid_right_node]
    lower_hyperedge_neighbors = [mid_right_node, lower_right_node, (image.width // 2 - 1, 0)]
    add_hyperedge_edges(graph, upper_hyperedge[0], upper_hyperedge_neighbors)
    add_hyperedge_edges(graph, lower_hyperedge[0], lower_hyperedge_neighbors)

    upper_b_nodes = [(uuid4(), 3 * image.width // 4, image.height - 1),
                     (uuid4(), image.width - 1, 3 * image.height // 4)]
    lower_b_nodes = [(uuid4(), image.width - 1, image.height // 4), (uuid4(), 3 * image.width // 4, 0)]
    add_b_nodes(upper_b_nodes, graph)
    add_b_nodes(lower_b_nodes, graph)

    add_hyperedge_edges(graph, upper_b_nodes[0][0], upper_hyperedge_neighbors[:-1])
    add_hyperedge_edges(graph, upper_b_nodes[1][0], upper_hyperedge_neighbors[1:])
    add_hyperedge_edges(graph, lower_b_nodes[0][0], lower_hyperedge_neighbors[:-1])
    add_hyperedge_edges(graph, lower_b_nodes[1][0], lower_hyperedge_neighbors[1:])

    plot(graph)
    return graph


def add_nodes(graph: Graph, image: Image, node_positions: List[Tuple[int, int]]) -> None:
    for node_position in node_positions:
        colors = image.getpixel(node_position)
        graph.add_node(get_node_id(node_position), x=node_position[0], y=node_position[1], is_hyperedge=False,
                       r=colors[0], g=colors[1], b=colors[2], )


def add_hyperedges_nodes(graph: Graph, hyperedges_details: List[Tuple[UUID, int, int]]) -> None:
    for hyperedge_details in hyperedges_details:
        graph.add_node(hyperedge_details[0], x=hyperedge_details[1], y=hyperedge_details[2], is_hyperedge=True,
                       label='I', should_break=0, )


def add_hyperedge_edges(graph: Graph, hyperedge_id: UUID, neighbors: List[Tuple[int, int]]) -> None:
    for neighbor in neighbors:
        graph.add_edge(hyperedge_id, get_node_id(neighbor))


def add_b_nodes(b_nodes: List[Tuple[UUID, int, int]], graph: Graph) -> None:
    for b_node in b_nodes:
        graph.add_node(b_node[0], x=b_node[1], y=b_node[2], is_hyperedge=True, label='B', )
