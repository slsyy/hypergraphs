from unittest import TestCase

import networkx as nx
from PIL import Image

from plot import plot
from productions import P1
from utils import IMAGE_PATH


class TestApprox(TestCase):
    def setUp(self):
        self.graph = nx.Graph()
        self.image = Image.open(IMAGE_PATH)
        width, height = self.image.size
        self.x_max_idx = width - 1
        self.y_max_idx = height - 1

    # TODO
    def test_preparation(self):
        P1(self.graph, self.x_max_idx, self.y_max_idx, self.image)
        plot(self.graph)
        # approx(self.image, 0, self.x_max_idx, 0, self.y_max_idx, ???)
