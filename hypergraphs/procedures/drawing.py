from PIL import Image


def draw(p1, p2, r1, r2, r3, r4, g1, g2, g3, g4, b1, b2, b3, b4):
    (x1, y1) = p1
    (x2, y2) = p2

    approx_r = [[0 for x in range(x2 + 1)] for y in range(y2 + 1)]
    approx_g = [[0 for x in range(x2 + 1)] for y in range(y2 + 1)]
    approx_b = [[0 for x in range(x2 + 1)] for y in range(y2 + 1)]

    for px in range(x1, x2 + 1):
        for py in range(y1, y2 + 1):
            avg_x = (px - x1) / (x2 - x1)
            avg_y = (py - y1) / (y2 - y1)

            factor1 = (1 - avg_x) * avg_y
            factor2 = avg_x * avg_y
            factor3 = (1 - avg_x) * (1 - avg_y)
            factor4 = avg_x * (1 - avg_y)

            approx_r[px][py] += r1 * factor1
            approx_g[px][py] += g1 * factor1
            approx_b[px][py] += b1 * factor1

            approx_r[px][py] += r2 * factor2
            approx_g[px][py] += g2 * factor2
            approx_b[px][py] += b2 * factor2

            approx_r[px][py] += r3 * factor3
            approx_g[px][py] += g3 * factor3
            approx_b[px][py] += b3 * factor3

            approx_r[px][py] += r4 * factor4
            approx_g[px][py] += g4 * factor4
            approx_b[px][py] += b4 * factor4

    for x in range(x1, x2 + 1):
        for y in range(y1, y2 + 1):
            approx_r[x][y] = int(round(approx_r[x][y]))
            approx_g[x][y] = int(round(approx_g[x][y]))
            approx_b[x][y] = int(round(approx_b[x][y]))

    bitmap = Image.new('RGB', (x2 + 1, y2 + 1), "black")
    pixels = bitmap.load()
    for x in range(x2 + 1):
        for y in range(y2 + 1):
            pixels[x, y] = (approx_r[x][y], approx_g[x][y], approx_b[x][y])
    # bitmap.show()

    return approx_r, approx_g, approx_b
