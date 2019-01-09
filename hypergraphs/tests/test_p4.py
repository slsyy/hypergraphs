import os
import uuid
from unittest import TestCase

from matplotlib import pyplot as plt
import networkx as nx
from PIL import Image

from productions import P1
from productions import P2
from productions import P3
from productions import P4
from productions import P5

from utils import HyperEdge, IMAGE_PATH, Direction

from plot import plot_but_dont_show
from utils import *


IMAGE_PATH = os.path.join(os.path.dirname(
    __file__), "test_data", "four_colors.jpg")

B_DIRECTION_EDGE_LAMBDAS = {
    Direction.N: lambda data, f_data: f_data['x'] == data['x'] and f_data['y'] < data['y'],
    Direction.S: lambda data, f_data: f_data['x'] == data['x'] and f_data['y'] > data['y'],
    Direction.E: lambda data, f_data: f_data['x'] < data['x'] and f_data['y'] == data['y'],
    Direction.W: lambda data, f_data: f_data['x'] > data['x'] and f_data['y'] == data['y'],
}


class TestP4(TestCase):
    def setUp(self):
        self.graph = nx.Graph()
        self.image = Image.open(IMAGE_PATH)

    def test_p4(self):
        width, height = self.image.size

        P1(self.graph, x_max_idx=width - 1,
           y_max_idx=height - 1, image=self.image)
        i_hyperedges_ids = self.__hyperedges_ids(HyperEdge.I)
        P5(self.graph, i_hyperedges_ids[0], self.image)
        P2(self.graph, i_hyperedges_ids[0], self.image)

        i_hyperedges_ids = self.__hyperedges_ids(HyperEdge.I)
        for i_hyperedge in i_hyperedges_ids[:3]:
            P5(self.graph, i_hyperedge, self.image)

        self.hyp_fs = [(x, y) for x, y in self.graph.nodes(
            data=True) if 'label' in y.keys() and y['label'] in [d.name for d in Direction]]
        self.hyp_bs = [(x, y) for x, y in self.graph.nodes(
            data=True) if 'label' in y.keys() and y['label'] == 'B']
        self.hyp_is = [(x, y) for x, y in self.graph.nodes(
            data=True) if 'label' in y.keys() and y['label'] == 'I']
        self.hyperedges = {
            Direction.N: {},
            Direction.S: {},
            Direction.E: {},
            Direction.W: {},
        }
        for direction, edges in self.hyperedges.items():
            edges['f'] = [x for x in self.hyp_fs if x[1]
                          ['label'] == direction.name][0]
            edges['b'] = [(x, y) for x, y in self.hyp_bs if B_DIRECTION_EDGE_LAMBDAS[direction](
                y, edges['f'][1])][0]

            f_neighbour = list(self.graph.neighbors(edges['f'][0]))[0]
            b_neighbours = list(self.graph.neighbors(edges['b'][0]))
            edges['is'] = []
            for x, y in self.graph.nodes(data=True):
                if 'label' in y and y['label'] == 'I':
                    i_neighbours = list(self.graph.neighbors(x))

                    if f_neighbour in i_neighbours and (b_neighbours[0] in i_neighbours or b_neighbours[1] in i_neighbours):
                        edges['is'].append((x, y))

        for _, edges in self.hyperedges.items():
            P3(self.graph, edges['b'][0], [
               x for x, y in edges['is']], edges['f'][0], self.image)

        for i_hyperedge in i_hyperedges_ids[:3]:
            P2(self.graph, i_hyperedge, self.image)

        graph_before = self.graph.copy()
        N = [i for i, d in self.graph.nodes(data=True) if d.get(
            "label", None) == "N" and d["y"] == 299.0][0]
        P4(self.graph, N, self.image)

        W = [i for i, d in self.graph.nodes(data=True) if d.get(
            "label", None) == "W" and d["x"] == 99.0][0]
        P4(self.graph, W, self.image)
        graph_after = self.graph

        plt.subplot(121)
        plt.title("Before")
        plot_but_dont_show(graph_before)

        plt.subplot(122)
        plt.title("After")
        plot_but_dont_show(graph_after)
        plt.show()

    def __hyperedges_ids(self, label):
        return [idd for idd, data in self.__hyperedges(label)]

    def __hyperedges(self, label):
        return [(idd, data) for idd, data in self.graph.nodes(data=True)
                if 'label' in data.keys() and data['label'] == label.name]
