from unittest import TestCase
from hypergraphs.procedures import drawing


class TestDrawing(TestCase):
    def testFullColors(self):
        p1 = (0, 0)
        p2 = (100, 100)
        (x1, y1) = p1
        (x2, y2) = p2

        drawing.draw(p1, p2, 255, 0, 0, 255, 0, 255, 0, 255, 0, 0, 255, 0)

        approx_r = [[255 for x in range(x1, x2 + 1)] for y in range(y1, y2 + 1)]
        approx_g = [[0 for x in range(x1, x2 + 1)] for y in range(y1, y2 + 1)]
        approx_b = [[0 for x in range(x1, x2 + 1)] for y in range(y1, y2 + 1)]

        received_approx_r, received_approx_g, received_approx_b = drawing.draw(p1, p2, 255, 255, 255, 255, 0, 0, 0, 0, 0, 0, 0, 0)

        self.assertEqual((approx_r, approx_g, approx_b), (received_approx_r, received_approx_g, received_approx_b))

        approx_r = [[0 for x in range(x1, x2 + 1)] for y in range(y1, y2 + 1)]
        approx_g = [[255 for x in range(x1, x2 + 1)] for y in range(y1, y2 + 1)]
        approx_b = [[0 for x in range(x1, x2 + 1)] for y in range(y1, y2 + 1)]

        received_approx_r, received_approx_g, received_approx_b = drawing.draw(p1, p2, 0, 0, 0, 0, 255, 255, 255, 255, 0, 0, 0, 0)

        self.assertEqual((approx_r, approx_g, approx_b), (received_approx_r, received_approx_g, received_approx_b))

        approx_r = [[0 for x in range(x1, x2 + 1)] for y in range(y1, y2 + 1)]
        approx_g = [[0 for x in range(x1, x2 + 1)] for y in range(y1, y2 + 1)]
        approx_b = [[255 for x in range(x1, x2 + 1)] for y in range(y1, y2 + 1)]

        received_approx_r, received_approx_g, received_approx_b = drawing.draw(p1, p2, 0, 0, 0, 0, 0, 0, 0, 0, 255, 255, 255, 255)

        self.assertEqual((approx_r, approx_g, approx_b), (received_approx_r, received_approx_g, received_approx_b))

        approx_r = [[255 for x in range(x1, x2 + 1)] for y in range(y1, y2 + 1)]
        approx_g = [[255 for x in range(x1, x2 + 1)] for y in range(y1, y2 + 1)]
        approx_b = [[255 for x in range(x1, x2 + 1)] for y in range(y1, y2 + 1)]

        received_approx_r, received_approx_g, received_approx_b = drawing.draw(p1, p2, 255, 255, 255, 255, 255, 255, 255, 255,  255, 255, 255, 255)

        self.assertEqual((approx_r, approx_g, approx_b), (received_approx_r, received_approx_g, received_approx_b))

        approx_r = [[0 for x in range(x1, x2 + 1)] for y in range(y1, y2 + 1)]
        approx_g = [[0 for x in range(x1, x2 + 1)] for y in range(y1, y2 + 1)]
        approx_b = [[0 for x in range(x1, x2 + 1)] for y in range(y1, y2 + 1)]

        received_approx_r, received_approx_g, received_approx_b = drawing.draw(p1, p2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

        self.assertEqual((approx_r, approx_g, approx_b), (received_approx_r, received_approx_g, received_approx_b))
