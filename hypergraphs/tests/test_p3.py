from unittest import TestCase

import networkx as nx
from PIL import Image

from hypergraphs.productions import P1, P2, P3
from hypergraphs.utils import get_node_id, IMAGE_PATH, Direction

B_DIRECTION_EDGE_LAMBDAS = {
    Direction.N: lambda data, f_data: f_data['x'] == data['x'] and f_data['y'] < data['y'],
    Direction.S: lambda data, f_data: f_data['x'] == data['x'] and f_data['y'] > data['y'],
    Direction.E: lambda data, f_data: f_data['x'] < data['x'] and f_data['y'] == data['y'],
    Direction.W: lambda data, f_data: f_data['x'] > data['x'] and f_data['y'] == data['y'],
}


class TestP3(TestCase):
    def setUp(self):
        self.graph = nx.Graph()
        self.image = Image.open(IMAGE_PATH)
        width, height = self.image.size
        P1(self.graph, x_max_idx=width - 1, y_max_idx=height - 1, image=self.image)
        hyperedge = [(x, y) for x, y in self.graph.nodes(data=True) if 'label' in y.keys() and y['label'] == 'I'][0]
        hyperedge[1]['should_break'] = 1
        self.graph.add_node(hyperedge[0], **hyperedge[1])
        P2(self.graph, hyperedge_id=hyperedge[0], image=self.image)

        # plot(self.graph)

        self.hyp_fs = [(x, y) for x, y in self.graph.nodes(data=True) if
                       'label' in y.keys() and y['label'] in [d.name for d in Direction]]
        self.hyp_bs = [(x, y) for x, y in self.graph.nodes(data=True) if 'label' in y.keys() and y['label'] == 'B']
        self.hyp_is = [(x, y) for x, y in self.graph.nodes(data=True) if 'label' in y.keys() and y['label'] == 'I']
        self.hyperedges = {
            Direction.N: {},
            Direction.S: {},
            Direction.E: {},
            Direction.W: {},
        }
        for direction, edges in self.hyperedges.items():
            edges['f'] = [x for x in self.hyp_fs if x[1]['label'] == direction.name][0]
            edges['b'] = [(x, y) for x, y in self.hyp_bs if B_DIRECTION_EDGE_LAMBDAS[direction](y, edges['f'][1])][0]

            f_neighbour = list(self.graph.neighbors(edges['f'][0]))[0]
            b_neighbours = list(self.graph.neighbors(edges['b'][0]))
            edges['is'] = []
            for x, y in self.graph.nodes(data=True):
                if 'label' in y and y['label'] == 'I':
                    i_neighbours = list(self.graph.neighbors(x))

                    if f_neighbour in i_neighbours and (
                            b_neighbours[0] in i_neighbours or b_neighbours[1] in i_neighbours):
                        edges['is'].append((x, y))

        # for direction, edges in self.hyperedges.items():
        #     P3(self.graph, edges['b'][0], [x for x, y in edges['is']], edges['f'][0], self.image)
        #     plot(self.graph)
        # import ipdb;
        # ipdb.set_trace()

    def test_if_exception_when_wrong_b_hyperedge(self):
        dir_N = self.hyperedges[Direction.N]
        dir_S = self.hyperedges[Direction.S]
        dir_E = self.hyperedges[Direction.E]

        def raisingMethod():
            P3(self.graph, dir_S['b'][0], [x for x, y in dir_N['is']], dir_N['f'][0], self.image)

        self.assertRaises(ValueError, raisingMethod)

        def raisingMethod2():
            P3(self.graph, dir_E['b'][0], [x for x, y in dir_N['is']], dir_N['f'][0], self.image)

        self.assertRaises(ValueError, raisingMethod2)

    def test_if_exception_when_wrong_f_hyperedge(self):
        dir_N = self.hyperedges[Direction.N]
        dir_S = self.hyperedges[Direction.S]

        def raisingMethod():
            P3(self.graph, dir_N['b'][0], [x for x, y in dir_N['is']], dir_S['f'][0], self.image)

        self.assertRaises(ValueError, raisingMethod)

    def test_b_hyperedge_removed(self):
        edges = self.hyperedges[Direction.N]
        self.run_P3(edges)
        self.assertTrue(edges['b'][0] not in self.graph.node)

    def test_v_created(self):
        edges = self.hyperedges[Direction.N]
        self.run_P3(edges)
        bx, by = edges['b'][1]['x'], edges['b'][1]['y']
        new_node_id = get_node_id((bx, by))

        self.assertTrue(new_node_id in self.graph.node)

    def test_v_connected_with_b_hyperedges(self):
        edges = self.hyperedges[Direction.N]
        self.run_P3(edges)
        bx, by = edges['b'][1]['x'], edges['b'][1]['y']
        new_node_id = get_node_id((bx, by))

        neighbours = list(self.graph.neighbors(new_node_id))
        bs = [(x, y) for x, y in self.graph.nodes(data=True) if
              x in neighbours and 'label' in y.keys() and y['label'] == 'B']
        self.assertTrue(len(bs) == 2)

    def test_v_connected_with_i_hyperedges(self):
        edges = self.hyperedges[Direction.N]
        self.run_P3(edges)
        bx, by = edges['b'][1]['x'], edges['b'][1]['y']
        new_node_id = get_node_id((bx, by))

        neighbours = list(self.graph.neighbors(new_node_id))
        self.assertTrue(edges['is'][0][0] in neighbours)
        self.assertTrue(edges['is'][1][0] in neighbours)

    def test_v_connected_with_f_hyperedge(self):
        edges = self.hyperedges[Direction.N]
        self.run_P3(edges)
        bx, by = edges['b'][1]['x'], edges['b'][1]['y']
        new_node_id = get_node_id((bx, by))

        neighbours = list(self.graph.neighbors(new_node_id))
        self.assertTrue(edges['f'][0] in neighbours)

    ### HELPERS

    def run_P3(self, edges):
        P3(self.graph, edges['b'][0], [x for x, y in edges['is']], edges['f'][0], self.image)
