from typing import List

import numpy as np

from colors.color import RGB


def lerp(t: float, i_min: float, i_max: float, o_min: float, o_max: float):
    return (t - i_min) * (o_max - o_min) / (i_max - i_min) + o_min


def lerp_01(t: float, out_min: float, out_max: float):
    return t * (out_max - out_min) / 1 + out_min


def color_gradient(col_a: RGB, col_b: RGB, steps: int) -> List[RGB]:
    return [lerp_color(x, col_a, col_b) for x in np.arange(0, 1, 1 / steps)]


def lerp_color(t: float, color_a: RGB, color_b: RGB) -> RGB:
    return RGB(int(color_a.r + (color_b.r - color_a.r) * t),
               int(color_a.g + (color_b.g - color_a.g) * t),
               int(color_a.b + (color_b.b - color_a.b) * t))
