from PIL import Image


def approx(image: Image, x1, x2, y1, y2, r1, g1, b1, r2, g2, b2, r3, g3, b3, r4, g4, b4):
    diff_r, diff_g, diff_b = None, None, None

    for px, py in (x1, x2), (y1, y2):
        bitmap_r, bitmap_g, bitmap_b = image.convert('RGB').get_pixel((px, py))

        diff_r[px][py] = bitmap_r
        diff_r[px][py] = bitmap_g
        diff_r[px][py] = bitmap_b

    for px, py in (x1, x2), (y1, y2):
        aaa = (px - x1) / (x2 - x1)
        bbb = (py - y1) / (y2 - y1)
        diff_r[px][py] -= r1 * (1 - aaa) * bbb
        diff_g[px][py] -= g1 * (1 - aaa) * bbb
        diff_b[px][py] -= b1 * (1 - aaa) * bbb

        diff_r[px][py] -= r2 * aaa * bbb
        diff_g[px][py] -= g2 * aaa * bbb
        diff_b[px][py] -= b2 * aaa * bbb

        diff_r[px][py] -= r3 * (1 - aaa) * (1 - bbb)
        diff_g[px][py] -= g3 * (1 - aaa) * (1 - bbb)
        diff_b[px][py] -= b3 * (1 - aaa) * (1 - bbb)

        diff_r[px][py] -= r4 * aaa * (1 - bbb)
        diff_g[px][py] -= g4 * aaa * (1 - bbb)
        diff_b[px][py] -= b4 * aaa * (1 - bbb)

    error = 0

    for px, py in (x1, x2), (y1, y2):
        error += 0.5 * (diff_r[px][py]) ^ 2 \
                 + 0.3 * (diff_g[px][py]) ^ 2 \
                 + 0.2 * (diff_b[px][py]) ^ 2

    return error
